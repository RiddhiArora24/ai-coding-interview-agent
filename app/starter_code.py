import json


def infer_cpp_type(values):

    value = None

    for item in values:
        if item is not None:
            value = item

        if isinstance(item, list) and len(item) > 0:
            value = item
            break

    if value is None:
        return "int"

    if isinstance(value, bool):
        return "bool"

    if isinstance(value, int):
        return "int"

    if isinstance(value, float):
        return "double"

    if isinstance(value, str):
        return "string"

    if isinstance(value, list):

        nested_values = []

        for candidate in values:

            if isinstance(candidate, list):

                nested_values.extend(
                    candidate
                )

        inner = infer_cpp_type(
            nested_values
            if nested_values
            else [0]
        )

        return f"vector<{inner}>"

    return "int"


def python_starter(question):

    first_case = question["test_cases"][0]

    args = list(
        first_case["input"].keys()
    )

    args_text = ", ".join(args)

    return f'''def solve({args_text}):
    # Write your solution here
    pass
'''


def cpp_starter(question):

    test_cases = question["test_cases"]

    first_case = test_cases[0]

    arg_names = list(
        first_case["input"].keys()
    )

    arguments = []

    for name in arg_names:

        samples = [
            case["input"].get(name)
            for case in test_cases
        ]

        cpp_type = infer_cpp_type(
            samples
        )

        arguments.append(
            f"{cpp_type} {name}"
        )

    return_samples = [
        case["expected"]
        for case in test_cases
    ]

    return_type = infer_cpp_type(
        return_samples
    )

    params = ", ".join(arguments)

    return f'''{return_type} solve({params}) {{
    // Write your solution here

}}
'''


def get_starter_code(question):

    return {
        "python": python_starter(
            question
        ),
        "cpp": cpp_starter(
            question
        )
    }
