import json
import math
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


PYTHON_TIMEOUT = 5
CPP_COMPILE_TIMEOUT = 15
CPP_RUN_TIMEOUT = 5


def values_equal(
    actual,
    expected,
    judge="exact"
):

    if judge == "unordered":

        try:
            return sorted(
                actual,
                key=lambda x: repr(x)
            ) == sorted(
                expected,
                key=lambda x: repr(x)
            )

        except Exception:
            return False

    if judge == "unordered_nested":

        try:

            actual_norm = [
                sorted(
                    item,
                    key=lambda x: repr(x)
                )
                for item in actual
            ]

            expected_norm = [
                sorted(
                    item,
                    key=lambda x: repr(x)
                )
                for item in expected
            ]

            actual_norm = sorted(
                actual_norm,
                key=lambda x: repr(x)
            )

            expected_norm = sorted(
                expected_norm,
                key=lambda x: repr(x)
            )

            return actual_norm == expected_norm

        except Exception:
            return False

    if isinstance(expected, float):

        try:
            return math.isclose(
                float(actual),
                expected,
                rel_tol=1e-6,
                abs_tol=1e-6
            )

        except Exception:
            return False

    return actual == expected


# ============================================================
# PYTHON
# ============================================================

def run_python_case(
    code,
    test_input
):

    wrapper = f'''
import json

{code}

data = json.loads(input())

try:
    result = solve(**data)
    print(json.dumps({{
        "ok": True,
        "result": result
    }}))
except Exception as error:
    print(json.dumps({{
        "ok": False,
        "error": type(error).__name__ + ": " + str(error)
    }}))
'''

    with tempfile.TemporaryDirectory() as temp:

        file_path = Path(temp) / "candidate.py"

        file_path.write_text(
            wrapper,
            encoding="utf-8"
        )

        try:

            process = subprocess.run(
                [
                    os.sys.executable,
                    str(file_path)
                ],
                input=json.dumps(
                    test_input
                ),
                capture_output=True,
                text=True,
                timeout=PYTHON_TIMEOUT,
                cwd=temp
            )

        except subprocess.TimeoutExpired:

            return {
                "ok": False,
                "error": "Time Limit Exceeded"
            }

        output = process.stdout.strip()

        if not output:

            error = process.stderr.strip()

            return {
                "ok": False,
                "error": error or "No output produced."
            }

        lines = output.splitlines()

        try:

            result = json.loads(
                lines[-1]
            )

            return result

        except Exception:

            return {
                "ok": False,
                "error": (
                    process.stderr.strip()
                    or "Your program printed invalid output."
                )
            }


# ============================================================
# C++
# ============================================================

def cpp_literal(value):

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        return repr(value)

    if isinstance(value, str):
        return json.dumps(value)

    if isinstance(value, list):

        values = ", ".join(
            cpp_literal(item)
            for item in value
        )

        return "{" + values + "}"

    raise ValueError(
        f"Unsupported C++ input: {type(value)}"
    )


CPP_HELPERS = r'''
#include <bits/stdc++.h>
using namespace std;

string jsonEscape(const string& s) {
    string out;

    for (char c : s) {
        if (c == '\\') out += "\\\\";
        else if (c == '"') out += "\\\"";
        else if (c == '\n') out += "\\n";
        else if (c == '\r') out += "\\r";
        else if (c == '\t') out += "\\t";
        else out += c;
    }

    return out;
}

void printJson(const string& value) {
    cout << "\"" << jsonEscape(value) << "\"";
}

void printJson(const char* value) {
    printJson(string(value));
}

void printJson(bool value) {
    cout << (value ? "true" : "false");
}

template <typename T>
typename enable_if<is_integral<T>::value && !is_same<T, bool>::value>::type
printJson(const T& value) {
    cout << value;
}

template <typename T>
typename enable_if<is_floating_point<T>::value>::type
printJson(const T& value) {
    cout << setprecision(15) << value;
}

template <typename T>
void printJson(const vector<T>& values) {

    cout << "[";

    for (size_t i = 0; i < values.size(); i++) {

        if (i > 0)
            cout << ",";

        printJson(values[i]);
    }

    cout << "]";
}
'''


def build_cpp_source(
    code,
    test_cases
):

    calls = []

    for index, case in enumerate(
        test_cases
    ):

        args = []

        for value in case["input"].values():

            args.append(
                cpp_literal(value)
            )

        call = ", ".join(args)

        calls.append(
            f'''
    try {{
        auto result_{index} = solve({call});
        cout << "RESULT:";
        printJson(result_{index});
        cout << "\\n";
    }}
    catch (const exception& error) {{
        cout << "ERROR:"
             << error.what()
             << "\\n";
    }}
'''
        )

    main_body = "\n".join(calls)

    return f'''
{CPP_HELPERS}

{code}

int main() {{

{main_body}

    return 0;
}}
'''


def run_cpp(
    code,
    test_cases
):

    compiler = shutil.which("g++")

    if not compiler:

        return {
            "compiler_missing": True,
            "error": (
                "g++ was not found. "
                "Install MinGW-w64 or another g++ compiler "
                "to enable C++ execution."
            )
        }

    source = build_cpp_source(
        code,
        test_cases
    )

    with tempfile.TemporaryDirectory() as temp:

        source_file = Path(temp) / "main.cpp"
        exe_file = Path(temp) / "main.exe"

        source_file.write_text(
            source,
            encoding="utf-8"
        )

        try:

            compile_result = subprocess.run(
                [
                    compiler,
                    "-std=c++17",
                    "-O2",
                    str(source_file),
                    "-o",
                    str(exe_file)
                ],
                capture_output=True,
                text=True,
                timeout=CPP_COMPILE_TIMEOUT,
                cwd=temp
            )

        except subprocess.TimeoutExpired:

            return {
                "compile_error": True,
                "error": "Compilation timed out."
            }

        if compile_result.returncode != 0:

            return {
                "compile_error": True,
                "error": compile_result.stderr[-4000:]
            }

        try:

            process = subprocess.run(
                [str(exe_file)],
                capture_output=True,
                text=True,
                timeout=CPP_RUN_TIMEOUT,
                cwd=temp
            )

        except subprocess.TimeoutExpired:

            return {
                "runtime_error": True,
                "error": "Time Limit Exceeded"
            }

        lines = process.stdout.splitlines()

        outputs = []

        for line in lines:

            if line.startswith("RESULT:"):

                raw = line[
                    len("RESULT:"):
                ]

                try:
                    outputs.append({
                        "ok": True,
                        "result": json.loads(raw)
                    })

                except Exception:
                    outputs.append({
                        "ok": False,
                        "error": "Invalid output format."
                    })

            elif line.startswith("ERROR:"):

                outputs.append({
                    "ok": False,
                    "error": line[
                        len("ERROR:"):
                    ]
                })

        return {
            "outputs": outputs,
            "stderr": process.stderr
        }


# ============================================================
# COMPLETE SUBMISSION
# ============================================================

def run_submission(
    question,
    code,
    language,
    visible_only=False
):

    all_cases = question["test_cases"]

    if visible_only:
        test_cases = all_cases[:2]
    else:
        test_cases = all_cases

    judge = question.get(
        "judge",
        "exact"
    )

    results = []


    # --------------------------------------------------------
    # PYTHON
    # --------------------------------------------------------

    if language == "python":

        for number, case in enumerate(
            test_cases,
            start=1
        ):

            execution = run_python_case(
                code,
                case["input"]
            )

            if not execution.get("ok"):

                results.append({
                    "test": number,
                    "passed": False,
                    "error": execution.get(
                        "error",
                        "Runtime error"
                    )
                })

                continue

            actual = execution.get(
                "result"
            )

            passed = values_equal(
                actual,
                case["expected"],
                judge
            )

            result = {
                "test": number,
                "passed": passed,
                "actual": actual
            }

            if visible_only:

                result["input"] = case["input"]
                result["expected"] = case["expected"]

            results.append(result)


    # --------------------------------------------------------
    # C++
    # --------------------------------------------------------

    elif language == "cpp":

        execution = run_cpp(
            code,
            test_cases
        )

        if execution.get("compiler_missing"):

            return {
                "language": language,
                "passed": 0,
                "total": len(test_cases),
                "success": False,
                "compiler_missing": True,
                "error": execution["error"],
                "tests": []
            }

        if execution.get("compile_error"):

            return {
                "language": language,
                "passed": 0,
                "total": len(test_cases),
                "success": False,
                "compile_error": True,
                "error": execution["error"],
                "tests": []
            }

        if execution.get("runtime_error"):

            return {
                "language": language,
                "passed": 0,
                "total": len(test_cases),
                "success": False,
                "runtime_error": True,
                "error": execution["error"],
                "tests": []
            }

        outputs = execution.get(
            "outputs",
            []
        )

        for index, case in enumerate(
            test_cases
        ):

            number = index + 1

            if index >= len(outputs):

                results.append({
                    "test": number,
                    "passed": False,
                    "error": "No result produced."
                })

                continue

            output = outputs[index]

            if not output.get("ok"):

                results.append({
                    "test": number,
                    "passed": False,
                    "error": output.get(
                        "error",
                        "Runtime error"
                    )
                })

                continue

            actual = output["result"]

            passed = values_equal(
                actual,
                case["expected"],
                judge
            )

            result = {
                "test": number,
                "passed": passed,
                "actual": actual
            }

            if visible_only:

                result["input"] = case["input"]
                result["expected"] = case["expected"]

            results.append(result)

    else:

        return {
            "language": language,
            "passed": 0,
            "total": len(test_cases),
            "success": False,
            "error": "Unsupported language.",
            "tests": []
        }


    passed_count = sum(
        1
        for result in results
        if result["passed"]
    )

    return {
        "language": language,
        "passed": passed_count,
        "total": len(test_cases),
        "success": passed_count == len(
            test_cases
        ),
        "tests": results
    }
