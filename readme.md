# sdrtf
Framework for unit testing in Sun Devil Rocketry firmware.

EXTERNAL DEPENDENCIES:
- GNU C Compiler (GCC). If you're used to our embedded environment, it's a different version of GCC for testing, you need to build for your own hardware.
- GNU GCov. This should be included in whatever gives you access to GCC. We use this to generate the coverage reports that tell developers how often a given statement or branch is hit. GDB is also highly recommended.
- GCovr (simply do pip install gcovr, then add it to your PATH. Alternatively, if you're on linux, you can use your preferred package manager).
- A bash terminal of some kind. Git Bash is recommended on Windows, and most Linux terminals should do. The makefiles use bash commands during execution to achieve the desired terminal and file output.

GETTING STARTED:
- Remember to correctly clone the submodule into your test repo.
- If this is your first time writing or modifying a unit test for SDR, take a look at some others to get an example!
- If you need to create a new test, there is no tool to do this yet. Try copying an existing test or ask me (@etsells) for help.
- When modifying a test, pay close attention to the coverage report and the results.
- Tests should be written using POSIX interfaces. Windows syscalls will break tests for Linux users!
