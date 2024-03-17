import tempfile
import subprocess
import json
import os
from utility import replace_class_name_in_code, write_code_to_file, compile_java, execute_java, get_data, predict_class, beautify_java_stderr, get_suggestions
import re


def check_result(result, expected):
    # Check if the result is an error
    if convert_result(result) == 2:
        return 'Error'
    # Check if the result matches the expected value
    elif convert_result(result) == expected:
        return True
    else:
        return False


def convert_result(result):
    # Define regular expressions to match prime-related patterns
    regex = r"(\bis\s|is\sa\s)\bprime\b"
    regex2 = r"\b(not|isn't)\b.*\bprime\b"

    # Check if the result is empty or doesn't match any prime-related pattern
    if result == "" or (not re.search(regex, result, re.IGNORECASE) and not re.search(regex2, result, re.IGNORECASE)):
        return 2
    # Check if the result matches the first prime-related pattern
    elif re.search(regex, result, re.IGNORECASE):
        return 1
    else:
        return 0

# def convert_result(result):
#     positive_keywords = ["is a prime", "is prime"]
#     negative_keywords = ["is not a prime", "isn't a prime", "is not prime", "isn't prime"]


def process_json_data(temp_file_name, json_data, specific_question_id):
    results = []
    result_array = []
    expected_array = []

    for data in json_data:
        if data['QuestionID'] == specific_question_id:
            correct_results = data['CorrectResult']
            for index, value in enumerate(correct_results):
                stdin = str(index+1)
                expected = value
                expected_array.append(expected)

                try:
                    execute_process = execute_java(temp_file_name, stdin)
                    result = {
                        'stdin': stdin,
                        'stdout': execute_process.stdout.strip(),
                        # 'stderr': execute_process.stderr.strip(),
                        'pass': check_result(execute_process.stdout.strip(), expected),
                        'result': convert_result(execute_process.stdout.strip()),
                        'expected': expected
                    }

                    results.append(result)
                    result_array.append(convert_result(
                        execute_process.stdout.strip()))
                except subprocess.TimeoutExpired:
                    return {'Error': 'The Java process timed out'}, None, None

    return results, result_array, expected_array


def primary_number(request_data):
    code = request_data

    json_data = json.loads(get_data("Question"))
    for item in json_data:
        # Convert the 'CorrectResult' string into an int array
        item['CorrectResult'] = json.loads(item['CorrectResult'])
    temp_file = tempfile.NamedTemporaryFile(
        suffix='.java', delete=False, dir='.', prefix='q1_')
    temp_file_name = os.path.basename(temp_file.name[:-5])

    new_code = replace_class_name_in_code(code, temp_file_name)
    write_code_to_file(temp_file.name, new_code)

    compile_process = compile_java(temp_file_name)
    # print(compile_process.stderr.strip())
    # print(compile_process.stdout.strip())
    # print(compile_process.returncode)

    if compile_process.returncode == 0:
        results, result_array, expected_array = process_json_data(
            temp_file_name, json_data, 1)
        if results is None:
            return result_array  # This is an error message

        # print(result_array)
        # print(expected_array)
        # print(len(result_array) == len(expected_array))
        # print(result_array != expected_array)
        if len(result_array) == len(expected_array):
            if result_array != expected_array:
                predict, distance = predict_class(result_array, 1)
                new_json = get_suggestions(1, predict)
                prediction_json = {
                    'prediction': [
                        {'class': int(predict)},
                        {'distance': int(distance)}
                    ]
                }
                response = {'results': results,
                            'prediction': int(predict)}
                response.update(prediction_json)
                response.update(new_json)

            else:
                response = {'results': results}
    else:
        error_message = compile_process.stderr.strip()
        response = json.loads(beautify_java_stderr(error_message))

    return response, temp_file.name
