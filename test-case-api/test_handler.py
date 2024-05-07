import json
import os
import shutil
from utility import write_code_to_file, compile_java, predict_class, beautify_java_stderr, get_suggestions, run_testcase, ensure_path_exists
from database_handler import get_data_json

CLASS_EXTENSION = '.class'  # Constant that defines the extension for Java class files


def setup_paths(question_id, student_id, is_submitted=None):
    # Fetch question data from the database
    question_data = json.loads(get_data_json(
        'Questions', None, f'QuestionID = {question_id}'))
    # Base directory for data storage
    base_path = os.path.join(os.getcwd(), 'data')

    # Decide the directory path based on whether the submission is final
    if not is_submitted:
        file_path = os.path.join(base_path, 'student', student_id, f'q{
                                 question_data[0]["QuestionID"]}')
    else:
        file_path = os.path.join(base_path, 'student', student_id, f'q{
                                 question_data[0]["QuestionID"]}', 'submitted')

    ensure_path_exists(file_path)  # Ensure the file path exists
    # Get the filename from question data
    file_name = question_data[0]['QuestionFileName']

    # Initialize paths for the driver if needed
    driver_path = ''
    driver_name = ''
    if question_data[0]['DriverType'] > 0:
        driver_path = os.path.join(base_path, 'teacher', question_data[0]['TeacherID'], f'q{
                                   question_data[0]["QuestionID"]}', 'driver')
        ensure_path_exists(driver_path)
        driver_name = question_data[0]['QuestionDriverName']

    return question_data[0], file_path, file_name, driver_path, driver_name


def handle_driver(file_path, file_name, driver_path, driver_name, need_driver):
    # Determine the target file path
    target_file = os.path.join(file_path, file_name)
    if need_driver > 0:
        # If a driver is needed, update the target file path and copy the driver
        target_file = os.path.join(file_path, driver_name)
        shutil.copyfile(os.path.join(driver_path, driver_name), target_file)
    print(target_file)  # Output the path of the target file
    return compile_java(target_file, file_path)  # Compile the Java file


def test_entry(question_id, request_data, student_id, is_submitted=None):
    code = request_data  # Code submitted by the student
    # Set up necessary paths and retrieve configuration
    question_data, file_path, file_name, driver_path, driver_name = setup_paths(
        question_id, student_id, is_submitted)
    need_driver = question_data['DriverType']

    write_code_to_file(os.path.join(file_path, file_name),
                       code)  # Write code to the file

    print("Start compile")
    # Handle driver and compile code
    compile_process = handle_driver(
        file_path, file_name, driver_path, driver_name, need_driver)
    # Check for compilation errors
    if compile_process.returncode != 0:
        error_message = compile_process.stderr.strip()
        return json.loads(beautify_java_stderr(error_message))

    print("Finish compile")
    test_result_file = os.path.join(
        file_path, driver_name if need_driver > 0 else file_name)
    # Run test cases and capture results
    results, result_array, expected_array = run_testcase(
        test_result_file, file_path, question_data)

    # Return error message if results are not available
    if results is None:
        return result_array

    # Clean up files if not a final submission
    if not is_submitted:
        if need_driver:
            clean_up_files(file_path, file_name, driver_name)
        else:
            clean_up_files(file_path, file_name)
    print(result_array)
    print(expected_array)

    # Generate response based on test results
    response_data = generate_response(
        result_array, expected_array, results, question_data)
    return response_data


def clean_up_files(file_path, file_name, driver_name=None):
    # Remove generated files to clean up the directory
    os.remove(os.path.join(file_path, file_name))
    os.remove(os.path.join(file_path, file_name[:-5] + CLASS_EXTENSION))
    if driver_name:
        os.remove(os.path.join(file_path, driver_name))
        os.remove(os.path.join(file_path, driver_name[:-5] + CLASS_EXTENSION))


def generate_response(result_array, expected_array, results, question_data):
    # Initialize the response dictionary with common data
    response = {'results': results, 'result_array': result_array}

    # Check if the result_array matches the expected_array
    if len(result_array) != len(expected_array) or result_array != expected_array:
        predict, distance = predict_class(
            result_array, question_data['QuestionID'])
        new_json = get_suggestions(question_data['QuestionID'], predict)
        prediction_json = {
            'prediction': [{'class': int(predict)}, {'distance': int(distance)}]
        }
        # Update the response with prediction and suggestions
        response.update(prediction_json)
        response.update(new_json)

    return response
