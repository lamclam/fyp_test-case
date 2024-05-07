import os
import re
import json
import subprocess
import ast
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from database_handler import get_data_json
from string_handler import separate_keywords, separate_testcase, check_any_phrase, compare_result
from typing import List, Dict, Any


# Function to remove a file if it exists
def remove_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)


# Function to replace the class name in a given piece of Java code
def replace_class_name_in_code(code, new_class_name):
    class_name = re.search(r'class\s+(\w+)', code).group(1)
    return code.replace(class_name, new_class_name)


# Function to replace a specific name in the code with a new name
def replace_name_in_code(code, target, new_name):
    target_name = re.search(r'(\b' + target + r'\b)', code).group(1)
    return code.replace(target_name, new_name)


# Function to write Java code to a file
def write_code_to_file(temp_file_path, code):
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(code)


# Function to compile Java code using `javac`
def compile_java(temp_file_name, working_path):
    return subprocess.run(['javac', temp_file_name], capture_output=True, text=True, cwd=working_path)


# Function to execute a Java program and capture its output
def execute_java(temp_file_name, working_path, stdin='', timeout=15):
    result = subprocess.run(['java', temp_file_name], input=stdin,
                            capture_output=True, text=True, timeout=timeout, cwd=working_path)
    return result


# Function to compare two lists and return the differences
def compare_lists(list1, list2):
    differences = []
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            differences.append((i, list1[i], list2[i]))
    return differences


# Function to format and beautify Java compilation errors
def beautify_java_stderr(stderr_string):
    pattern = r"(.*\.java):(\d+): error: (.*)$"
    matches = re.findall(pattern, stderr_string, re.MULTILINE)
    print(stderr_string)
    errors = [{"File": match[0], "Line": match[1], "Error": match[2]}
              for match in matches] if matches else [{"Error": stderr_string}]
    error_dict = {"Error": errors}
    return json.dumps(error_dict, indent=4)


# Function to predict the class of new data using KNeighborsClassifier
def predict_class(new_x, question_id):
    json_data = get_data_json("KNNClasses")
    data = json.loads(json_data)
    for item in data:
        item['KNNClassData'] = json.loads(item['KNNClassData'])
    classes = []
    features = []
    for item in data:
        if item['QuestionID'] == question_id:
            features.append([int(i) for i in item['KNNClassData']])
            classes.append(item['KNNClass'])
    if not features:
        return None, None
    x = np.array(features)
    classes = np.array(classes)
    knn = KNeighborsClassifier(n_neighbors=1, metric='hamming')
    knn.fit(x, classes)
    new_point = np.array([new_x]).reshape(1, -1)
    prediction = knn.predict(new_point)
    _distances, indices = knn.kneighbors(new_point)
    nearest_point = x[indices[0][0]].astype(int)
    new_point_int = new_point.astype(int)
    return prediction[0], sum(el1 != el2 for el1, el2 in zip(new_point_int[0], nearest_point))


# Function to retrieve suggestions based on a question ID and case set
def get_suggestions(question_id: int, case_set: int):
    suggestion = json.loads(get_data_json(
        "KNNClasses", None, f"QuestionID = {question_id}"))
    matched_case_sets = set()
    all_suggestions = []
    for d in suggestion:
        case_set_numbers = int(d['KNNClass'])
        if case_set == case_set_numbers and d['KNNClass'] not in matched_case_sets:
            all_suggestions.extend(d['KNNClassSuggestion'].split(' | '))
            matched_case_sets.add(d['KNNClass'])
    return {'suggestion': all_suggestions}


# Function to convert a result based on detected keywords
def convert_result(sentence, question_id):
    key_words = json.loads(get_data_json(
        'QuestionKeyWords', None, f'QuestionID = {question_id}'))
    positive_keywords, negative_keywords = separate_keywords(key_words)
    if not sentence:
        return 2
    if not positive_keywords or not negative_keywords:
        raise ValueError("The Keywords list is empty")
    if check_any_phrase(positive_keywords, sentence):
        return 1
    elif check_any_phrase(negative_keywords, sentence):
        return 0
    else:
        return 2


# Function to run a Java program for specific test cases and compare the results
def run_testcase(temp_file_name, working_path, json_data):
    results = []
    result_array = []
    expected_array = []
    correct_results = ast.literal_eval(json_data['CorrectResult'])
    test_case_data = get_data_json('TestCases', None, f'QuestionID = {
                                   json_data['QuestionID']}')
    test_case_array = separate_testcase(json.loads(test_case_data))
    for index, number in enumerate(test_case_array):
        if index < len(correct_results):
            stdin = str(number)
            expected = correct_results[index]
            expected_array.append(expected)
            try:
                execute_process = execute_java(
                    temp_file_name, working_path, stdin)
                result_number = convert_result(
                    execute_process.stdout.strip(), json_data['QuestionID'])
                result = {'stdin': stdin, 'stdout': execute_process.stdout.strip(), 'isCorrect': compare_result(
                    result_number, expected), 'result': result_number, 'expected': expected}
                results.append(result)
                result_array.append(result_number)
            except subprocess.TimeoutExpired:
                return {'Error': 'The Java process timed out'}, None, None
        else:
            break
    return results, result_array, expected_array


# Function to ensure a directory path exists, and create it if it doesn't
def ensure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


# Function to calculate the Hamming distance between two lists of integers
def hamming_distance(s1: List[int], s2: List[int]) -> int:
    if len(s1) != len(s2):
        raise ValueError("Lists must be of the same length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


# Function to cluster test cases based on Hamming distance and return the results in JSON format
def cluster_test_cases(test_cases: List[Dict[str, Any]], threshold: int) -> str:
    n = len(test_cases)
    clusters = []
    used = [False] * n
    for test_case in test_cases:
        test_case["ParsedResult"] = json.loads(test_case["TestCaseResult"])
    for i in range(n):
        if not used[i]:
            cluster = [test_cases[i]]
            used[i] = True
            for j in range(i + 1, n):
                if not used[j]:
                    dist = hamming_distance(
                        test_cases[i]["ParsedResult"], test_cases[j]["ParsedResult"])
                    if dist <= threshold:
                        cluster.append(test_cases[j])
                        used[j] = True
            clusters.append(cluster)
    for cluster in clusters:
        for item in cluster:
            del item["ParsedResult"]
    result = json.dumps(clusters, indent=2)
    return result
