#!/usr/bin/env python
import sys
import pytest

PYTEST_ARGS = ['invaana_scout','tests', '--cov=invaana_scout', '--tb=short', '-rw' ]


def exit_on_failure(command, message=None):
    if command:
        sys.exit(command)


def run_tests_coverage():
    if __name__ == "__main__":
        pytest.main(PYTEST_ARGS)

exit_on_failure(run_tests_coverage())