"""Run Otter-Grader OK-format checks under Pyodide/JupyterLite, without otter-grader.

Standard library only -- no pip install, no micropip, no network. This is
deliberately a small reimplementation of one piece of otter-grader:
student-facing `check()`/`check_all()` against public test cases. Everything
else in the real package -- otter assign, generate, run, grade, PDF export,
logging, environment serialization, plugins, Gradescope integration -- is out
of scope on purpose and stays on a machine with a real Python: full
otter-grader hard-depends on Docker and a real browser process for those
(see AUDIT.md, 2026-08-08), which cannot exist inside a WASM sandbox, and
even setting that aside, none of it is needed to give a student a pass/fail
result on the public tests. Grade the hidden tests locally with real
otter-grader; author with `otter assign` as usual (`tests: files: true` in
the assignment config) so this stays a read-only consumer of its output.

Input format: reads exactly what `otter assign` writes to a chapter's
`tests/` directory -- a `.py` file with `OK_FORMAT = True` and a `test =
{...}` dict (name, suites -> cases -> code/hidden/name). Loading (exec the
file, read test_globals['test']) and case execution (stdlib `doctest`,
parsing each case's `code` as a doctest string and running it against the
caller's globals) both mirror otter-grader's own
`otter.test_files.ok_test.OKTestFile` (BSD-3-Clause, UC Berkeley Division of
Data Science and Information) line for line in approach, not by accident --
matching it is what makes the conformance guarantee below possible. Multiple
suites per file and non-empty setup/teardown aren't supported, matching
OKTestFile's own restrictions (both are rejected explicitly, not silently
ignored).

Real otter's own `OKTestFile.run()` does NOT filter by `hidden` -- it runs
every case it's given. That's safe there because `otter assign` never
distributes hidden cases to students in the first place (confirmed by
generating a real assignment and diffing the student vs. autograder test
files). check() below skips `hidden` cases anyway, as a defensive second
layer with no real-otter behavior to be conformant *with* -- it only matters
if a fuller test file (e.g. an autograder copy) ends up somewhere a student
can reach it by mistake.

Conformance with real otter-grader (same test files, same submission,
same pass/fail) is verified by jupyterlite/check_conformance.py, run against
a real `pip install otter-grader` locally. Do not change the execution logic
here without rerunning it.

    check("q1")            # tests/q1.py, against the caller's globals
    check_all()             # every tests/*.py, in name order
"""
import doctest
import glob
import inspect
import io
import os
from contextlib import redirect_stderr, redirect_stdout
from textwrap import dedent, indent

__all__ = ["check", "check_all", "CheckResult"]


class CheckResult:
    """The result of checking one question: a name and a list of per-case results.

    Each case result is ``(case_name, passed, message)``; ``message`` is the
    doctest failure detail (expected vs. actual) when ``passed`` is False,
    else an empty string.
    """

    def __init__(self, name, case_results):
        self.name = name
        self.case_results = case_results

    @property
    def passed_all(self):
        return all(passed for _, passed, _ in self.case_results)

    def __repr__(self):
        if not self.case_results:
            return f"{self.name}: no visible test cases"
        if self.passed_all:
            return f"{self.name} passed! \U0001f389"
        lines = [f"{self.name} results:"]
        for case_name, passed, message in self.case_results:
            lines.append(f"  {'✅' if passed else '❌'} {case_name}")
            if not passed:
                lines.append(indent(message.rstrip(), "      "))
        return "\n".join(lines)

    def _repr_html_(self):
        if not self.case_results:
            return f"<p><strong>{self.name}</strong>: no visible test cases</p>"
        if self.passed_all:
            return f"<p><strong>{self.name}</strong> passed! \U0001f389</p>"
        parts = [f"<p><strong style='color:#b00'>{self.name}</strong> results:</p>"]
        for case_name, passed, message in self.case_results:
            icon = "✅" if passed else "❌"
            parts.append(f"<p>{icon} <code>{case_name}</code></p>")
            if not passed:
                parts.append(f"<pre style='margin-left:1.5em'>{message.rstrip()}</pre>")
        return "".join(parts)


def _load_test_spec(path):
    test_globals = {}
    with open(path) as f:
        exec(compile(f.read(), path, "exec"), test_globals)
    if "test" not in test_globals:
        raise ValueError(f"{path} does not define 'test'")
    return test_globals["test"]


def _run_doctest_case(name, code, global_env):
    """Run one case's doctest-formatted code against global_env.

    Mirrors otter.test_files.ok_test.run_doctest: parse the case body as a
    doctest, run it with verbose=True so failures capture expected-vs-actual,
    and report pass/fail from the runner's own summary rather than any
    exception escaping (an AssertionError inside a doctest is a normal
    failure, not a crash).
    """
    examples = doctest.DocTestParser().parse(code, name)
    test = doctest.DocTest(
        [e for e in examples if isinstance(e, doctest.Example)],
        global_env,
        name,
        None,
        None,
        code,
    )
    runner = doctest.DocTestRunner(verbose=True)
    output = io.StringIO()
    with redirect_stdout(output), redirect_stderr(output):
        runner.run(test, clear_globs=False)
    with open(os.devnull, "w") as devnull, redirect_stdout(devnull), redirect_stderr(devnull):
        summary = runner.summarize(verbose=True)
    return summary.failed == 0, output.getvalue()


def _run_spec(spec, global_env):
    suites = spec["suites"]
    if len(suites) != 1:
        raise ValueError(f"{spec['name']}: only a single test suite is supported")
    suite = suites[0]
    if suite.get("type", "doctest") != "doctest":
        raise ValueError(f"{spec['name']}: only doctest-type suites are supported")
    if suite.get("setup") or suite.get("teardown"):
        raise ValueError(f"{spec['name']}: setup/teardown are not supported")

    case_results = []
    for i, case in enumerate(suite["cases"]):
        if case.get("hidden", True):
            continue
        case_name = case.get("name", f"{spec['name']} - {i + 1}")
        code = dedent(case["code"])
        try:
            passed, message = _run_doctest_case(case_name, code, global_env)
        except Exception as e:
            passed, message = False, f"{type(e).__name__}: {e}"
        case_results.append((case_name, passed, message))

    return CheckResult(spec["name"], case_results)


def check(name, tests_dir="tests", global_env=None):
    """Check `name` (e.g. "q1") against `{tests_dir}/{name}.py`.

    global_env defaults to the caller's globals, so a student sees results
    for the variables and functions they just defined -- pass an explicit
    dict to check against something else (e.g. from check_all(), or a test).
    """
    path = os.path.join(tests_dir, name + ".py")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Test {name!r} does not exist at {path}")

    if global_env is None:
        global_env = inspect.currentframe().f_back.f_globals

    return _run_spec(_load_test_spec(path), global_env)


def check_all(tests_dir="tests", global_env=None):
    """Check every `{tests_dir}/*.py`, in name order. Returns a list of CheckResult."""
    if global_env is None:
        global_env = inspect.currentframe().f_back.f_globals

    names = sorted(
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(tests_dir, "*.py"))
    )
    return [check(name, tests_dir=tests_dir, global_env=global_env) for name in names]
