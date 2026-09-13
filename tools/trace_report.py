#!/usr/bin/env python3
"""Generate a Markdown requirements-to-test-results traceability report."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


RESULT_TAG_PATTERN = re.compile(
    r"(?:Requirement Tag|Requirements):\s*(?P<tag>\S+)"
)
ANALYSIS_RESULT_PATTERN = re.compile(
    r"\|\s*`(?P<tag>RQ\.[^`]+)`\s*\|.*?\|\s*"
    r"(?:<[^>]+>)*\s*(?P<status>PASS|FAIL)\s*(?:<[^>]+>)*\s*\|",
    re.IGNORECASE,
)
FAIL_PATTERN = re.compile(r"^\s*Fails:\s*(?P<count>\d+)\s*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate trace-report.md from requirement and test-results files."
    )
    parser.add_argument(
        "--req-format",
        required=True,
        help=(
            "Regex applied to requirement lines. The first capture group must be "
            "the requirement tag and the second must be the requirement text."
        ),
    )
    parser.add_argument(
        "--spec-files",
        required=True,
        help="Regex matching requirement-document paths relative to the current directory.",
    )
    parser.add_argument(
        "--results-files",
        required=True,
        help="Regex matching test-results paths relative to the search root.",
    )
    parser.add_argument(
        "--search-root",
        type=Path,
        default=Path.cwd(),
        help="Directory to search for spec and results files (default: current directory).",
    )
    return parser.parse_args()


def matching_files(root: Path, pattern: re.Pattern[str]) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and pattern.search(path.relative_to(root).as_posix())
    )


def load_requirements(
    files: list[Path], requirement_pattern: re.Pattern[str], root: Path
) -> list[tuple[str, str]]:
    requirements: list[tuple[str, str]] = []
    for path in files:
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            match = requirement_pattern.search(line)
            if not match or not match.group(1).strip() or not match.group(2).strip():
                continue
            if match.lastindex is None or match.lastindex < 2:
                raise ValueError(
                    "--req-format must contain two capture groups: tag and requirement text."
                )
            tag = match.group(1).strip()
            text = match.group(2).strip()
            if not text:
                raise ValueError(
                    f"Requirement {tag} has no requirement text "
                    f"({path.relative_to(root).as_posix()}:{line_number})."
                )
            requirements.append((tag, text))
    return requirements


def load_results(files: list[Path], root: Path) -> dict[str, list[tuple[str, bool]]]:
    traces: dict[str, list[tuple[str, bool]]] = {}
    for path in files:
        content = path.read_text(encoding="utf-8")
        result_path = path.relative_to(root).as_posix()
        failed = any(int(match.group("count")) > 0 for match in FAIL_PATTERN.finditer(content))
        for match in RESULT_TAG_PATTERN.finditer(content):
            traces.setdefault(match.group("tag"), []).append((result_path, failed))
        for match in ANALYSIS_RESULT_PATTERN.finditer(content):
            traces.setdefault(match.group("tag"), []).append(
                (result_path, match.group("status").upper() == "FAIL")
            )
    return traces


def generate_report(
    requirements: list[tuple[str, str]], traces: dict[str, list[tuple[str, bool]]]
) -> str:
    missing = sorted({tag for tag, _ in requirements if tag not in traces})
    report: list[str] = ["# Requirements Traceability Report", ""]
    if missing:
        report.append(
            '<span style="color: #b45309"><strong>Warning:</strong> The following '
            "requirements do not trace to a test results file: "
            + ", ".join(f"`{tag}`" for tag in missing)
            + ".</span>"
        )
        report.append("")

    report.extend(
        [
            "| Requirement tag | Requirement text | Results file | Test status |",
            "| --- | --- | --- | --- |",
        ]
    )
    for tag, text in requirements:
        matches = traces.get(tag)
        if not matches:
            report.append(
                f'| <span style="color: #b45309">`{tag}`</span> | '
                f'<span style="color: #b45309">{text}</span> | '
                f'<span style="color: #b45309">Not traced</span> | '
                f'<span style="color: #b45309">TRACE ISSUE</span> |'
            )
            continue
        result_paths = "<br>".join(f"`{result_path}`" for result_path, _ in matches)
        status = "FAIL" if any(failed for _, failed in matches) else "PASS"
        status_color = "#b91c1c" if status == "FAIL" else "#15803d"
        report.append(
            f"| `{tag}` | {text} | {result_paths} | "
            f'<span style="color: {status_color}"><strong>{status}</strong></span> |'
        )
    report.append("")
    return "\n".join(report)


def main() -> int:
    args = parse_args()
    try:
        requirement_pattern = re.compile(args.req_format)
        spec_pattern = re.compile(args.spec_files)
        results_pattern = re.compile(args.results_files)
        output_dir = Path.cwd()
        search_root = args.search_root.resolve()
        spec_files = matching_files(search_root, spec_pattern)
        result_files = matching_files(search_root, results_pattern)
        requirements = load_requirements(spec_files, requirement_pattern, search_root)
        traces = load_results(result_files, search_root)
        (output_dir / "trace-report.md").write_text(
            generate_report(requirements, traces), encoding="utf-8"
        )
    except (OSError, re.error, ValueError) as error:
        print(f"trace_report.py: error: {error}")
        return 2

    print(f"Wrote trace-report.md ({len(requirements)} requirements, {len(result_files)} result files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
