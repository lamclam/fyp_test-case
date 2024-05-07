import re
import ast


def separate_keywords(data):
    # Initialize empty lists to store positive and negative keywords
    positive_keywords = []
    negative_keywords = []

    # Loop through each dictionary in the input list `data`
    for item in data:
        # Retrieve the keyword and its type from each dictionary
        keyword = item['QuestionKeyWord']
        word_type = item['WordType']

        # If `WordType` is positive, append to positive_keywords, else to negative_keywords
        if word_type > 0:
            positive_keywords.append(keyword)
        else:
            negative_keywords.append(keyword)

    # Return lists containing positive and negative keywords
    return positive_keywords, negative_keywords


def separate_testcase(data):
    # Initialize a list to hold test case values
    testcase = []

    # Loop through each dictionary in the input list `data`
    for item in data:
        # Append the value associated with the key 'TestCaseValue' to the testcase list
        testcase.append(item['TestCaseValue'])

    # Return the list of test case values
    return testcase


def check_any_phrase(phrases, sentence):
    # Raise an error if `phrases` list is empty
    if not phrases:
        raise ValueError("The Keywords list is empty")

    # Raise an error if `sentence` is empty
    if not sentence:
        raise ValueError("There is no inputted sentence")

    # Convert the input sentence to lowercase to facilitate case-insensitive comparison
    normalized_sentence = sentence.lower()

    # Check if any phrase from the list `phrases` is a substring of `sentence`
    for phrase in phrases:
        # Convert the phrase to lowercase
        normalized_phrase = phrase.lower()

        # If phrase is found in the sentence, return True
        if normalized_phrase in normalized_sentence:
            return True

    # If no phrases are found in the sentence, return False
    return False


def compare_result(str1, str2):
    # Compare `str1` with 2, if they are the same, return 'Error'
    if str1 == 2:
        return 'Error'
    # If `str1` and `str2` are equal, return True
    elif str1 == str2:
        return True
    # Otherwise, return False
    else:
        return False


def clean_string(input_string):
    # Use regex to find all integers in the input string
    integers = re.findall(r'\b\d+\b', input_string)
    # Convert the found strings of digits to integers and return
    return [int(i) for i in integers]


def calculate_similarity(a_str, b_str):
    # Convert JSON-like strings to Python lists using `ast.literal_eval`
    a = ast.literal_eval(a_str)
    b = ast.literal_eval(b_str)

    # Return an error message if the arrays have different lengths
    if len(a) != len(b):
        return "Arrays have different lengths"

    # Calculate the number of non-matching elements between the two lists
    differences = sum(1 for x, y in zip(a, b) if x != y)

    # Calculate similarity as the number of matching elements
    result = len(a) - differences
    return result


def get_array_length(str):
    # Evaluate string representation of a list to a list and return its length
    return len(ast.literal_eval(str))
