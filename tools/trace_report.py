#!/usr/bin/env python3
"""Generate a Markdown requirements-to-test-results traceability report."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


RESULT_TAG_PATTERN = re.compile(
    r"(?:Requirement Tag|Requirements):\s*(?P<tags>[^\r\n]+)"
)
RESULT_REQUIREMENTS_SECTION_PATTERN = re.compile(
    r"^#{1,6}\s+Requirements\s*$\r?\n(?P<tags>.*?)(?=^#{1,6}\s|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
ANALYSIS_RESULT_PATTERN = re.compile(
    r"\|\s*`(?P<tag>RQ\.[^`]+)`\s*\|.*?\|\s*"
    r"(?:<[^>]+>)*\s*(?P<status>PASS|FAIL)\s*(?:<[^>]+>)*\s*\|",
    re.IGNORECASE,
)
FAIL_PATTERN = re.compile(r"^\s*Fails:\s*(?P<count>\d+)\s*$", re.MULTILINE)
REQUIREMENT_TAG_PATTERN = re.compile(r"RQ\.[A-Z]+(?:-[A-Z]+)*\.\d+")
TRACE_UP_PATTERN = re.compile(
    r"\(Trace:\s*(?P<tag>RQ\.[A-Z]+(?:-[A-Z]+)*\.\d+)\s*\)"
)
DERIVED_PATTERN = re.compile(r"\(Derived\)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate trace-report.md from requirement and test-results files."
    )
    parser.add_argument(
        "--req-format",
        action="append",
        required=True,
        help=(
            "Regex applied to requirement lines. The first capture group must be "
            "the requirement tag and the second must be the requirement text. "
            "May be specified more than once."
        ),
    )
    parser.add_argument(
        "--spec-files",
        action="append",
        required=True,
        help=(
            "Regex matching requirement-document paths relative to the current directory. "
            "May be specified more than once; documents are processed in argument order."
        ),
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
    files: list[Path], requirement_patterns: list[re.Pattern[str]]
) -> list[tuple[str, str, str]]:
    requirements: list[tuple[str, str, str]] = []
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            first_tag_match = REQUIREMENT_TAG_PATTERN.search(line)
            if not first_tag_match:
                continue
            match = next(
                (
                    pattern_match
                    for pattern in requirement_patterns
                    if (pattern_match := pattern.search(line[first_tag_match.start() :]))
                ),
                None,
            )
            if not match:
                continue
            tag = first_tag_match.group()
            text = match.group(2).strip()
            if not tag or not text:
                continue
            trace_up_match = TRACE_UP_PATTERN.search(line)
            trace_up = (
                trace_up_match.group("tag")
                if trace_up_match
                else "Derived" if DERIVED_PATTERN.search(line) else "N/A"
            )
            requirements.append((tag, trace_up, text))
    return requirements


def load_results(files: list[Path], root: Path) -> dict[str, list[tuple[str, bool]]]:
    traces: dict[str, list[tuple[str, bool]]] = {}
    for path in files:
        content = path.read_text(encoding="utf-8")
        result_path = path.relative_to(root).as_posix()
        failed = any(int(match.group("count")) > 0 for match in FAIL_PATTERN.finditer(content))
        for match in RESULT_TAG_PATTERN.finditer(content):
            for tag in REQUIREMENT_TAG_PATTERN.findall(match.group("tags")):
                traces.setdefault(tag, []).append((result_path, failed))
        for match in RESULT_REQUIREMENTS_SECTION_PATTERN.finditer(content):
            for tag in REQUIREMENT_TAG_PATTERN.findall(match.group("tags")):
                traces.setdefault(tag, []).append((result_path, failed))
        for match in ANALYSIS_RESULT_PATTERN.finditer(content):
            traces.setdefault(match.group("tag"), []).append(
                (result_path, match.group("status").upper() == "FAIL")
            )
    return traces


def generate_report(
    requirements: list[tuple[str, str, str]], traces: dict[str, list[tuple[str, bool]]]
) -> str:
    missing = sorted({tag for tag, _, _ in requirements if tag not in traces})
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
            "| Requirement tag | Trace Up | Requirement text | Results file | Test status |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for tag, trace_up, text in requirements:
        trace_up_display = f"`{trace_up}`" if trace_up.startswith("RQ.") else trace_up
        matches = traces.get(tag)
        if not matches:
            report.append(
                f'| <span style="color: #b45309">`{tag}`</span> | '
                f'<span style="color: #b45309">{trace_up_display}</span> | '
                f'<span style="color: #b45309">{text}</span> | '
                f'<span style="color: #b45309">Not traced</span> | '
                f'<span style="color: #b45309">TRACE ISSUE</span> |'
            )
            continue
        result_paths = "<br>".join(f"`{result_path}`" for result_path, _ in matches)
        status = "FAIL" if any(failed for _, failed in matches) else "PASS"
        status_color = "#b91c1c" if status == "FAIL" else "#15803d"
        report.append(
            f"| `{tag}` | {trace_up_display} | {text} | {result_paths} | "
            f'<span style="color: {status_color}"><strong>{status}</strong></span> |'
        )
    report.append("")
    return "\n".join(report)


def main() -> int:
    args = parse_args()
    try:
        requirement_patterns = [re.compile(pattern) for pattern in args.req_format]
        if any(pattern.groups < 2 for pattern in requirement_patterns):
            raise ValueError(
                "--req-format must contain two capture groups: tag and requirement text."
            )
        spec_patterns = [re.compile(pattern) for pattern in args.spec_files]
        results_pattern = re.compile(args.results_files)
        output_dir = Path.cwd()
        search_root = args.search_root.resolve()
        spec_files = list(
            dict.fromkeys(
                path
                for pattern in spec_patterns
                for path in matching_files(search_root, pattern)
            )
        )
        result_files = matching_files(search_root, results_pattern)
        requirements = load_requirements(spec_files, requirement_patterns)
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
