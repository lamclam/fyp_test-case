import re
import numpy as np
import json
from sklearn.neighbors import KNeighborsClassifier
from utility import get_data


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
