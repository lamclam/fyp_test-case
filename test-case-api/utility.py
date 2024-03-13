import os
import re
import json
import mariadb
import subprocess
import psutil
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Database connection details
host = "192.168.1.241"
port = 3306
user = "fyp"
password = "He1I0world"
database = "fyp"


def remove_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)


def replace_class_name_in_code(code, new_class_name):
    class_name = re.search(r'class\s+(\w+)', code).group(1)
    return code.replace(class_name, new_class_name)


def replace_name_in_code(code, target, new_name):
    target_name = re.search(r'(\b' + target + r'\b)', code).group(1)
    return code.replace(target_name, new_name)


def write_code_to_file(temp_file_path, code):
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(code)


def compile_java(temp_file_name):
    return subprocess.run(['javac', temp_file_name + '.java'], capture_output=True, text=True)


def execute_java(temp_file_name, stdin='', timeout=15):
    result = subprocess.run(['java', temp_file_name], input=stdin,
                            capture_output=True, text=True, timeout=timeout)
    return result


def compare_lists(list1, list2):
    differences = []
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            # Stores the index and the differing elements
            differences.append((i, list1[i], list2[i]))
    return differences


def beautify_java_stderr(stderr_string):
    # Regular expression to match the file name, line number and error message
    pattern = r"(.*\.java):(\d+): error: (.*)$"
    matches = re.findall(pattern, stderr_string, re.MULTILINE)

    # If matches are found, create a list of dictionaries with the error information
    if matches:
        errors = [{"File": match[0], "Line": match[1], "Error": match[2]}
                  for match in matches]
    # If no matches are found, create a single-item list with the raw stderr as the error message
    else:
        errors = [{"Error": stderr_string}]

    # Nest the list of errors inside a dictionary under the "error" key
    error_dict = {"Error": errors}

    # Convert the dictionary into a JSON string and return it
    return json.dumps(error_dict, indent=4)


def predict_class(new_x, question_id):
    # Retrieve data from the "KNNClasses" database
    json_data = get_data("KNNClasses")
    data = json.loads(json_data)
    for item in data:
        # Convert the 'CorrectResult' string into an int array
        item['ClassData'] = json.loads(item['ClassData'])
    # Separate the features and classes
    classes = []
    features = []
    for item in data:
        if item['QuestionID'] == question_id:
            features.append([int(i) for i in item['ClassData']])
            classes.append(item['Class'])

    # If no data found for the specific question ID, return None
    if not features:
        return None

    # Convert the features and classes to numpy arrays
    x = np.array(features)
    classes = np.array(classes)

    # Create and fit the KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(x, classes)

    # Reshape the new point into a 2D array
    new_point = np.array([new_x])

    # Predict the class of the new point
    prediction = knn.predict(new_point)

    return prediction


def get_suggestions(question_id: int, case_set: list):
    # Parse the JSON data
    suggestion = json.loads(
        get_data("QuestionSuggestions", None, f"QuestionID = {question_id}"))

    # Initialize a set to track which case sets we've already matched
    matched_case_sets = set()

    # Initialize the list to hold all our suggestions
    all_suggestions = []

    # Iterate through all the suggestions
    for d in suggestion:
        # Split the 'CaseSet' string into a list of integers
        case_set_numbers = {int(x) for x in d['CaseSet'].split(',')}

        # Check if any number in the input case_set list matches the 'CaseSet' numbers
        if any(num in case_set_numbers for num in case_set):
            # If we have not already matched this case set
            if d['CaseSet'] not in matched_case_sets:
                # Split the 'Suggestion' string into a list at ' | ' and extend the all_suggestions list
                all_suggestions.extend(d['Suggestion'].split(' | '))
                # Add this 'CaseSet' to the set of matched case sets to avoid duplicate suggestions
                matched_case_sets.add(d['CaseSet'])

    # Return the suggestions in the specified JSON format
    return {'suggestion': all_suggestions}


# Function to retrieve data from a table
def get_data(table_name, column_name=None, where_clause=None):
    # Check if table_name or column_name contains spaces
    if ' ' in table_name or (column_name is not None and ' ' in column_name):
        error = {"error": "Input should not contain spaces."}
        return json.dumps(error)

    try:
        # Establish a connection to the database
        conn = mariadb.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Choose which columns to select based on the column_name argument
        columns_to_select = column_name if column_name else "*"

        # Execute the SELECT query on the specified table and columns
        if where_clause:
            cursor.execute(
                f"SELECT {columns_to_select} FROM {table_name} WHERE {where_clause}")
        else:
            cursor.execute(f"SELECT {columns_to_select} FROM {table_name}")

        # Get the column names from the cursor description
        columns = [desc[0] for desc in cursor.description]

        # Fetch all rows from the cursor and convert them to dictionaries
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]

        # Convert the result to JSON format and return
        return json.dumps(result)

    except mariadb.Error as e:
        # Handle any database errors and return an error message
        error = {"error": str(e)}
        return json.dumps(error)

    finally:
        # Close the database connection in the finally block
        if conn:
            conn.close()
