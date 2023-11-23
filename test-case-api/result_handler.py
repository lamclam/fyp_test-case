import re
import numpy as np
import json
from sklearn.neighbors import KNeighborsClassifier
from database_handler import get_data


def predict_class(new_x):
    # Retrieve data from the "knn_data" database
    json_data = get_data("knn_data")
    data = json.loads(json_data)

    # Separate the features and classes
    classes = []
    features = []
    for item in data:
        features.append(eval(item['features']))
        classes.append(item['class'])

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
    regex2 = r"(\bnot(a|.*)|\bisn't(a|.*))\bprime\b"

    # Check if the result is empty or doesn't match any prime-related pattern
    if result == "" or (not re.search(regex, result, re.IGNORECASE) and not re.search(regex2, result, re.IGNORECASE)):
        return 2
    # Check if the result matches the first prime-related pattern
    elif re.search(regex, result, re.IGNORECASE):
        return 1
    else:
        return 0
