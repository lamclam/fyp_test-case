import tempfile
import subprocess
import json
import re
import os
from utility import replace_class_name_in_code, write_code_to_file, compile_java, execute_java, replace_name_in_code, get_data, beautify_java_stderr, get_suggestions


def clean_string(input_string):
    # Find all occurrences of integers in the string
    integers = re.findall(r'\b\d+\b', input_string)
    # Convert the result to integers and return
    return [int(i) for i in integers]


def void_result(test_file_stdout):
    # Split the string into individual test cases
    test_cases = test_file_stdout.split("***End Of Test Case***")

    # Define keywords
    negative_keywords = ["false", "not palindrome", "not a palindrome"]

    # Process each test case
    results = []
    for test_case in test_cases:
        # Normalize the test case string
        normalized_test_case = test_case.lower().strip()

        if any(keyword in normalized_test_case for keyword in negative_keywords):
            # If any positive keyword is in the test case string, the result is true
            results.append(0)
        elif normalized_test_case == "":
            # If the test case string is empty, the result is error
            results.append(2)
        else:
            # If any negative keyword is in the test case string, the result is false
            results.append(1)

    return results


def final_result(results_list):
    question_data = get_data('Question')
    # Parse data if it's a string
    if isinstance(question_data, str):
        question_data = json.loads(question_data)
    expected_list = []
    wrong_results = []
    for question in question_data:
        if question['QuestionID'] == 2:
            # Convert the CorrectResult string to a list of integers
            expected_list = json.loads(question['CorrectResult'])
            break

    results_json = {"results": []}
    for i in range(len(expected_list)):
        # if the expected result is not equal to the actual result
        if expected_list[i] != results_list[i]:
            wrong_results.append(i + 1)
        result_dict = {
            "expected": expected_list[i],
            "pass": expected_list[i] == results_list[i],
            "case": str(i + 1),
            "stdout": results_list[i]
        }
        results_json["results"].append(result_dict)

    return json.dumps(results_json), wrong_results


def palindrome(request_data):
    is_void = 'void' in request_data
    test_file_prefix = 'q2d' if is_void else 'q2'
    test_file_template = 'PalindromeTestVoid.java' if is_void else 'PalindromeTest.java'

    with tempfile.NamedTemporaryFile(suffix='.java', delete=False, dir='.', prefix=test_file_prefix) as test_file, \
            tempfile.NamedTemporaryFile(suffix='.java', delete=False, dir='.', prefix='q2') as code_file:

        test_file_name = os.path.splitext(os.path.basename(test_file.name))[0]
        code_file_name = os.path.splitext(os.path.basename(code_file.name))[0]

        with open(f'./test-case-api/{test_file_template}', 'r') as file:
            test_code = file.read()

        # Replace placeholder class names and objects with the actual file names
        test_code = test_code.replace('PalindromeTest', test_file_name) \
                             .replace('Palindrome p', f'{code_file_name} p') \
                             .replace('new Palindrome', f'new {code_file_name}')
        request_code = request_data.replace(
            'class Palindrome', f'class {code_file_name}')

        write_code_to_file(test_file.name, test_code)
        write_code_to_file(code_file.name, request_code)

        compile_test_result = compile_java(test_file_name)
        compile_code_result = compile_java(code_file_name)

        if compile_test_result.returncode == 0 and compile_code_result.returncode == 0:
            try:
                test_output = execute_java(test_file_name)
                test_output_content = void_result(
                    test_output.stdout) if is_void else clean_string(test_output.stdout)
                response, wrong_result_array = final_result(
                    test_output_content)
                response = json.loads(response)
                if wrong_result_array:
                    new_suggestions = get_suggestions(2, wrong_result_array)
                    response.update(new_suggestions or {})
            except subprocess.TimeoutExpired:
                response = {'Error': 'The Java process timed out'}
        else:
            error_message = compile_test_result.stderr.strip(
            ) if compile_test_result.returncode != 0 else compile_code_result.stderr.strip()
            response = json.loads(beautify_java_stderr(error_message))

        return response, test_file.name, code_file.name
