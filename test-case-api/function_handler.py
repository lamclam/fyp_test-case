# Import necessary libraries and modules
import ast
import os
import json
import database_handler
import utility
import test_handler
import string_handler


# Function to handle the submission of a student's answer
def submit(student_id, question_id, incorrect=None):
    try:
        # Load the question data from the database
        question_data = json.loads(database_handler.get_data_json(
            'Questions', None, f'QuestionID = {question_id}'))
        # Define the base path for student data
        base_path = os.path.join(os.getcwd(), 'data')
        # Construct the file path where the submission should be stored
        file_path = os.path.join(base_path, 'student', student_id, f'q{
            question_data[0]["QuestionID"]}', 'submitted')
        # Ensure the directory exists
        utility.ensure_path_exists(file_path)

        # Calculate the similarity or correctness of the submitted answer
        mark = string_handler.calculate_similarity(
            question_data[0]["CorrectResult"], incorrect)
        # If an incorrect answer is provided, save it and the calculated mark
        if incorrect:
            database_handler.add_new_record("TestCaseResults", ["StudentID", "QuestionID", "TestCaseResult", "Mark"], [
                                            student_id, question_id, incorrect, mark])
        else:
            # If no incorrect answer is provided, use a default calculation
            mark = string_handler.get_array_length(
                question_data[0]["CorrectResult"])
            database_handler.add_new_record("TestCaseResults", ["StudentID", "QuestionID", "TestCaseResult", "Mark"], [
                                            student_id, question_id, incorrect, mark])
        # Return a response indicating successful submission
        response = {'submitted': True}
        return response
    except Exception as e:
        # Handle exceptions by re-raising them
        raise Exception(str(e))


# Function to run tests for all students for a specific question
def batch_run(question_id):
    result_list = []
    # Load the question data
    question_data = json.loads(database_handler.get_data_json(
        'Questions', None, f'QuestionID = {question_id}'))

    # Define the root directory of student data
    root_dir = os.path.join(os.getcwd(), 'data', 'student')
    for student_id in os.listdir(root_dir):
        student_path = os.path.join(root_dir, student_id)
        # Ensure the path is a directory
        if os.path.isdir(student_path):
            submitted_folder_path = os.path.join(
                student_path, f'q{question_data[0]["QuestionID"]}', 'submitted')
            # Check if the 'submitted' folder exists
            if os.path.exists(submitted_folder_path) and os.path.isdir(submitted_folder_path):
                for file in os.listdir(submitted_folder_path):
                    file_path = os.path.join(submitted_folder_path, file)
                    # Process Java files
                    if file.endswith('.java'):
                        with open(file_path, 'r') as java_file:
                            java_code = java_file.read()
                        # Test the java code and get a response
                        response = test_handler.test_entry(
                            question_id, java_code, student_id, 1)
                        # Analyze the response and build the result list
                        if 'results' in response:
                            correct_count = sum(
                                1 for r in response['results'] if r.get('isCorrect', False))
                            total_case_count = len(response['results'])
                            student_result = {
                                "student_id": student_id,
                                "prediction": response.get('prediction', []),
                                "correct_count": correct_count,
                                "total_case_count": total_case_count
                            }
                            result_list.append(student_result)
    # Return the final JSON structure containing all results
    final_result = {"result": result_list}
    return final_result


# Function to retrieve a specific file based on user ID, file type, and question ID
def get_file(user_id, file_type, question_id):
    question_data = json.loads(database_handler.get_data_json(
        'Questions', None, f'QuestionID = {question_id}'))
    base_path = os.path.join(os.getcwd(), 'data')
    # Determine the file path based on the file type
    if file_type == "test_file":
        file_path = os.path.join(base_path, 'student', user_id, f'q{
            question_data[0]["QuestionID"]}', 'submitted')
        file_name = question_data[0]['QuestionFileName']
    elif file_type == "driver_file":
        file_path = os.path.join(base_path, 'teacher', question_data[0]['TeacherID'], f'q{
            question_data[0]["QuestionID"]}', 'driver')
        file_name = question_data[0]['QuestionDriverName']
    else:
        # Handle invalid file type
        raise ValueError("file_typeis not valid")

    # Check if the specified file exists and read it
    if file_path and file_name:
        file_fullpath = os.path.join(file_path, file_name)
        if os.path.exists(file_fullpath):
            with open(file_fullpath, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return None
    else:
        raise ValueError("Invalid value of request")


# Function to add a new user with a specified user type
def add_user(user_id, user_type):
    root_dir = os.path.join(os.getcwd(), 'data')
    path = os.path.join(root_dir, user_type, user_id)
    # Ensure the user directory exists
    utility.ensure_path_exists(path)


# Function to save a file uploaded by a user
def save_file(file_code, user_id, question_id):
    question_data = json.loads(database_handler.get_data_json(
        'Questions', None, f'QuestionID = {question_id}'))
    driver_name = question_data[0]["QuestionDriverName"]
    root_dir = os.path.join(os.getcwd(), 'data')
    path = os.path.join(root_dir, 'teacher', user_id,
                        f'q{question_id}', 'driver', driver_name)

    """Save the uploaded file to the specified path."""
    if file_code:
        utility.write_code_to_file(path, str(file_code))
        return driver_name
    return None


# Function to perform clustering on test case results below a certain threshold
def clustering(question_id, threshold=2):
    question_data = json.loads(database_handler.get_data_json(
        'Questions', None, f'QuestionID = {question_id}'))
    full_mark = len(ast.literal_eval(question_data[0]["CorrectResult"]))
    print(full_mark)
    testcase_result = json.loads(database_handler.get_data_json(
        "TestCaseResults", None, f" QuestionID = '{question_id}' AND Mark < '{full_mark}'"))
    print(testcase_result)
    return utility.cluster_test_cases(testcase_result, threshold)
