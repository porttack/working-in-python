#!/usr/bin/env python3
"""Conformance check: check.py's pass/fail must match real otter-grader's.

Not part of `make check` -- requires `pip install otter-grader` locally,
which pulls in Docker/Playwright/pandas/etc. that have no reason to be a
dependency of every session touching this repo. Run by hand after any change
to check.py's execution logic (never after a change that only touches
CheckResult's __repr__/_repr_html_ formatting, since those don't affect
pass/fail):

    python3 jupyterlite/check_conformance.py

For each fixture in check_conformance_fixtures/, runs one or more submissions
through both real otter-grader's OKTestFile and this repo's check.py against
identical starting globals, and compares pass/fail -- overall and per case
(catches a case-isolation bug that an overall-only comparison would miss).
Exits 1 and prints every mismatch if anything disagrees.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "check_conformance_fixtures"

sys.path.insert(0, str(HERE))
import check  # noqa: E402

try:
    from otter.test_files.ok_test import OKTestFile
except ImportError:
    print(
        "error: otter-grader is not installed -- pip install otter-grader "
        "(this script is not part of make check; see its docstring)",
        file=sys.stderr,
    )
    sys.exit(1)


def real_otter_result(fixture_name, global_env):
    path = str(FIXTURES / f"{fixture_name}.py")
    test = OKTestFile.from_file(path)
    test.run(dict(global_env))
    per_case = [tcr.passed for tcr in test.test_case_results]
    return test.passed_all, per_case


def shim_result(fixture_name, global_env):
    result = check.check(fixture_name, tests_dir=str(FIXTURES), global_env=dict(global_env))
    per_case = [passed for _, passed, _ in result.case_results]
    return result.passed_all, per_case


CASES = [
    (
        "q1_real_otter_assign",
        "correct sieve",
        {
            "sieve": lambda n: {
                i
                for i in range(2, n + 1)
                if all(i % p for p in range(2, int(i**0.5) + 1))
            }
        },
    ),
    (
        "q1_real_otter_assign",
        "broken sieve (always empty)",
        {"sieve": lambda n: set()},
    ),
    (
        "q_multiline",
        "correct greeting",
        {"greeting": "Hello,\nworld!"},
    ),
    (
        "q_multiline",
        "wrong greeting",
        {"greeting": "nope"},
    ),
    (
        "q_exception",
        "correct safe_divide (raises)",
        {"safe_divide": lambda a, b: a / b},
    ),
    (
        "q_exception",
        "broken safe_divide (swallows the error)",
        {"safe_divide": lambda a, b: 0},
    ),
    (
        "q_float",
        "correct average",
        {"average": lambda a, b: (a + b) / 2},
    ),
    (
        "q_float",
        "broken average (returns sum, not mean)",
        {"average": lambda a, b: a + b},
    ),
    (
        "q_multi_case",
        "correct square (middle case always fails: undefined name)",
        {"square": lambda x: x * x},
    ),
    (
        "q_multi_case",
        "broken square (every case fails)",
        {"square": lambda x: x + x},
    ),
]


def main():
    mismatches = []
    for fixture_name, label, global_env in CASES:
        real_passed, real_per_case = real_otter_result(fixture_name, global_env)
        shim_passed, shim_per_case = shim_result(fixture_name, global_env)

        ok = real_passed == shim_passed and real_per_case == shim_per_case
        status = "OK" if ok else "MISMATCH"
        print(
            f"[{status}] {fixture_name} -- {label}: "
            f"real={real_passed} {real_per_case}  shim={shim_passed} {shim_per_case}"
        )
        if not ok:
            mismatches.append((fixture_name, label))

    if mismatches:
        print(f"\n{len(mismatches)} mismatch(es):", file=sys.stderr)
        for fixture_name, label in mismatches:
            print(f"  - {fixture_name}: {label}", file=sys.stderr)
        return 1

    print(f"\nconformance: clean ({len(CASES)} submissions across "
          f"{len(set(c[0] for c in CASES))} fixtures)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
