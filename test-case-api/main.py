import functools
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import test_handler
import account_handler
import function_handler
import database_handler
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

CLASS_EXTENSION = '.class'
ERROR_KEY = 'Error'
CONTENT_TYPE = 'Content-Type'
TEXT_PLAIN = 'text/plain'


def validate_request(f):
    """Decorator to validate the request."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get(CONTENT_TYPE) != TEXT_PLAIN or not request.data:
            return jsonify({ERROR_KEY: 'Invalid request'}), 400
        return f(*args, **kwargs)
    return decorated_function


@app.route('/test', methods=['POST'])
@validate_request
def run_primary_number():
    """Runs the primary number function and returns a response."""
    try:
        question_id = request.args.get('question_id')
        student_id = request.args.get('student_id')
        request_data = request.data.decode('utf-8')
        response = test_handler.test_entry(
            question_id, request_data, student_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/getdata', methods=['GET'])
def get_database():
    """Returns the data from a specified table."""
    try:
        if not request.args.get('table_name'):
            return jsonify({ERROR_KEY: 'No target'}), 404
        else:
            table_name = request.args.get('table_name')
        column_name = request.args.get('column_name') or None
        where_column = request.args.get('where_column') or None
        where_target = request.args.get('where_target') or None
        if where_column and where_target:
            data = database_handler.get_data_json(table_name, column_name, f'{
                                                  where_column} = \"{where_target}\"')
        else:
            data = database_handler.get_data_json(
                table_name, column_name, None)

        if data:
            return json.loads(data)
        else:
            return jsonify({ERROR_KEY: 'No data found'}), 404
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    try:
        user_id = request.form['user_id']
        password = request.form['password']
        response = account_handler.login(user_id, password)
        student_data = database_handler.get_data_json(
            'Students', None, f'StudentID = \"{user_id}\"')
        teacher_data = database_handler.get_data_json(
            'Teachers', None, f'TeacherID = \"{user_id}\"')
        user_type = ""

        if student_data and not teacher_data:  # user_id is student
            user_type = 'student'
        elif not student_data and teacher_data:  # user_id is teacher
            user_type = 'teacher'
        else:
            return jsonify({ERROR_KEY: "The user ID or password is not correct"}), 400

        if user_type == 'student':
            user_data = json.loads(student_data)
            user_id = user_data[0]['StudentID']
        else:
            user_data = json.loads(teacher_data)
            user_id = user_data[0]['TeacherID']

        print(user_data)
        print(user_data[0]['Password'])
        if user_data[0]['Password'] == password:
            response = {'login': True,
                        'userName': user_data[0]['Name'],
                        'type': user_type,
                        "userID": user_id
                        }
            return response
        else:
            return jsonify({ERROR_KEY: "The user ID or password is not correct"}), 400
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/batchrun', methods=['GET'])
def batch_run():
    try:
        question_id = request.args.get('question_id')
        response = function_handler.batch_run(question_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/getfile', methods=['GET'])
def get_file():
    try:
        if request.args.get('type') and request.args.get('user_id') and request.args.get('question_id'):
            file_type = request.args.get('type')
            user_id = request.args.get('user_id')
            question_id = request.args.get('question_id')
            response = function_handler.get_file(
                user_id, file_type, question_id)
            if response is None:
                return jsonify({ERROR_KEY: 'File not found'}), 404
            return Response(response, mimetype='text/plain')
        else:
            return jsonify({ERROR_KEY: 'Invalid request'}), 400
    except ValueError as ve:
        return jsonify({ERROR_KEY: str(ve)}), 400
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/deleteuser', methods=['DELETE'])
def delete_user():
    try:
        if request.args.get('type') and request.args.get('user_id'):
            user_type = request.args.get('type')
            user_id = request.args.get('user_id')
            response = account_handler.delete_user(
                user_id, user_type)
            return jsonify(response)
        else:
            return jsonify({ERROR_KEY: 'Invalid request'}), 400
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/deleteknn', methods=['DELETE'])
def delete_knn():
    try:
        if request.args.get('type') and request.args.get('user_id'):
            user_type = request.args.get('type')
            user_id = request.args.get('user_id')
            response = account_handler.delete_user(
                user_id, user_type)
            return jsonify(response)
        else:
            return jsonify({ERROR_KEY: 'Invalid request'}), 400
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/addrecord', methods=['POST'])
def add_record():
    data = request.json
    table_name = data.get('table_name')
    columns = data.get('columns')
    values = data.get('values')
    user_type = request.args.get('adduser')
    quick_info = request.args.get('qi')

    if not all([table_name, columns, values]):
        return jsonify({ERROR_KEY: "Missing data for table_name, columns, or values"}), 400

    try:
        # Assuming add_new_record is already imported and configured correctly
        response = json.loads(database_handler.add_new_record(
            table_name, columns, values))
        if user_type == "student" or user_type == "teacher":
            function_handler.add_user(quick_info, user_type)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 500


@app.route('/updaterecord', methods=['PATCH'])
def update_record():
    data = request.json
    table_name = data.get('table_name')
    columns = data.get('columns')
    values = data.get('values')
    where_clause = data.get('where_clause')

    if not all([table_name, columns, values, where_clause]):
        return jsonify({ERROR_KEY: "Missing data for table_name, columns, values or where_clause"}), 400

    try:
        # Assuming add_new_record is already imported and configured correctly
        response = json.loads(database_handler.update_record(
            table_name, columns, values, where_clause))
        return jsonify(response), 200
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']

    user_id = request.args.get('userid')
    question_id = request.args.get('questionid')

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        file_content = file.read()
        function_handler.save_file(
            file_content.decode('utf-8'), user_id, question_id)
        return jsonify({"message": "File successfully processed and saved"}), 201
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 500

# Only use for demo


@app.route('/adduser', methods=['POST'])
def add_user():
    required_fields = ['user_id', 'user_name', 'user_type', 'password']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_type = request.form['user_type']
    user_password = request.form['password']

    try:
        if user_type == "teacher":
            result = database_handler.add_new_record("Teachers", ["TeacherID", "Password", "Name"], [
                user_id, user_password, user_name])
        elif user_type == "student":
            result = database_handler.add_new_record("Student", ["StudentID", "Password", "Name"], [
                user_id, user_password, user_name])
            function_handler.add_user(user_id, user_type)
        else:
            return jsonify({"error": "Invalid user type"}), 400

        return jsonify(json.load(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/addknn', methods=['POST'])
def add_knn():
    required_fields = ['question_id', 'knn_class', 'knn_array', 'suggestion']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    question_id = request.form['question_id']
    knn_class = request.form['knn_class']
    knn_array = request.form['knn_array']
    knn_suggestion = request.form['suggestion']

    try:
        result = database_handler.add_new_record("KNNClasses", ["QuestionID", "KNNClass", "KNNClassData", "KNNClassSuggestion"], [
            question_id, knn_class, knn_array, knn_suggestion])
        return jsonify(json.load(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/addtestcase', methods=['POST'])
def add_testcase():
    required_fields = ['question_id', 'testcase_value']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    question_id = request.form['question_id']
    testcase_value = request.form['testcase_value']

    try:
        result = database_handler.add_new_record("TestCases", ["QuestionID", "TestCaseValue"], [
            question_id, testcase_value])
        return jsonify(json.load(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/addkeyword', methods=['POST'])
def add_keyword():
    required_fields = ['question_id', 'keyword', 'type']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    question_id = request.form['question_id']
    keyword = request.form['keyword']
    type = request.form['type']

    try:
        result = database_handler.add_new_record("QuestionKeyWords", ["QuestionID", "QuestionKeyWord", "WordType"], [
            question_id, keyword, type])
        return jsonify(json.load(result)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/addquestion', methods=['POST'])
def add_question():
    # Check for required fields in form data
    required_fields = ['question_id', 'question_name', 'correct_result',
                       'teacher_id', 'driver_type', 'question_filename', 'p_word', 'n_word']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Retrieve form data
    question_id = request.form['question_id']
    question_name = request.form['question_name']
    correct_result = request.form['correct_result']
    teacher_id = request.form['teacher_id']
    driver_type = request.form['driver_type']
    question_filename = request.form['question_filename']
    p_keywords = request.form['p_word'].split(',')
    n_keywords = request.form['n_word'].split(',')

    # Handle driver type with optional driver name and file
    if int(driver_type) > 0:
        if 'question_drivername' not in request.form:
            return jsonify({"error": "Missing field: question_drivername"}), 400
        question_drivername = request.form['question_drivername']

        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Read and process the file
        try:
            file_content = file.read()
            function_handler.save_file(file_content.decode(
                'utf-8'), question_id, teacher_id)

            # Add the new record with driver name and file
            result = database_handler.add_new_record(
                "Questions",
                ["QuestionID", "QuestionName", "CorrectResult", "TeacherID",
                    "DriverType", "QuestionFileName", "QuestionDriverName"],
                [question_id, question_name, correct_result, teacher_id,
                    driver_type, question_filename, question_drivername]
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Add the new record without driver name and file
        try:
            result = database_handler.add_new_record(
                "Questions",
                ["QuestionID", "QuestionName", "CorrectResult",
                    "TeacherID", "DriverType", "QuestionFileName"],
                [question_id, question_name, correct_result,
                    teacher_id, driver_type, question_filename]
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Add keywords to the QuestionKeywords table
    try:
        for keyword in p_keywords:
            database_handler.add_new_record(
                "QuestionKeywords",
                ["QuestionID", "QuestionWord", "WordType"],
                [question_id, keyword.strip(), 1]
            )
        for keyword in n_keywords:
            database_handler.add_new_record(
                "QuestionKeywords",
                ["QuestionID", "QuestionWord", "WordType"],
                [question_id, keyword.strip(), 0]
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result), 200  # Assuming result is already a dictionary

# Only use for demo


@app.route('/updateuser', methods=['POST'])
def update_user():
    required_fields = ['user_id', 'user_name', 'user_type', 'password']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_type = request.form['user_type']
    user_password = request.form['password']

    try:
        if user_type == "teacher":
            result = database_handler.update_record("Teachers", ["TeacherID", "Password", "Name"], [
                user_id, user_password, user_name], f"TeacherID = '{user_id}'")
        elif user_type == "student":
            result = database_handler.update_record("Student", ["StudentID", "Password", "Name"], [
                user_id, user_password, user_name], f"StudentID = '{user_id}'")
        else:
            return jsonify({"error": "Invalid user type"}), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/updateknn', methods=['POST'])
def update_knn():
    required_fields = ['question_id', 'knn_class', 'knn_array', 'suggestion']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    question_id = request.form['question_id']
    knn_class = request.form['knn_class']
    knn_array = request.form['knn_array']
    knn_suggestion = request.form['suggestion']

    try:
        result = database_handler.update_record("KNNClasses", ["QuestionID", "KNNClass", "KNNClassData", "KNNClassSuggestion"], [
            question_id, knn_class, knn_array, knn_suggestion], f"QuestionID = '{question_id}' AND KNNClass = '{knn_class}'")
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/updatetestcase', methods=['POST'])
def update_testcase():
    required_fields = ['testcase_id', 'question_id', 'testcase_value']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    testcase_id = request.form['testcase_id']
    question_id = request.form['question_id']
    testcase_value = request.form['testcase_value']

    try:
        result = database_handler.update_record("TestCases", ["QuestionID", "TestCaseValue"], [
            question_id, testcase_value], f"TestCasesID = '{testcase_id}'")
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/updatekeyword', methods=['POST'])
def update_keyword():
    required_fields = ['keyword_id', 'question_id', 'keyword', 'type']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    keyword_id = request.form['keyword_id']
    question_id = request.form['question_id']
    keyword = request.form['keyword']
    type = request.form['type']

    try:
        result = database_handler.update_record("QuestionKeyWords", ["QuestionID", "QuestionKeyWord", "WordType"], [
            question_id, keyword, type], f"QuestionKeyWordID = '{keyword_id}'")
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only use for demo


@app.route('/updatequestion', methods=['POST'])
def update_question():
    required_fields = ['question_id', 'question_name', 'correct_result',
                       'teacher_id', 'driver_type', 'question_filename']
    if not all(field in request.form for field in required_fields):
        missing = [
            field for field in required_fields if field not in request.form]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    question_id = request.form['question_id']
    question_name = request.form['question_name']
    correct_result = request.form['correct_result']
    teacher_id = request.form['teacher_id']
    driver_type = request.form['driver_type']
    question_filename = request.form['question_filename']
    question_drivername = request.form.get(
        'question_drivername')  # Optional field

    try:
        if driver_type and int(driver_type) > 0:
            result = database_handler.update_record("Questions", ["QuestionID", "QuestionName", "CorrectResult", "TeacherID", "DriverType", "QuestionFileName", "QuestionDriverName"], [
                question_id, question_name, correct_result, teacher_id, driver_type, question_filename, question_drivername if question_drivername else ""], f"QuestionID = '{question_id}'")
        else:
            result = database_handler.update_record("Questions", ["QuestionID", "QuestionName", "CorrectResult", "TeacherID", "DriverType", "QuestionFileName"], [
                question_id, question_name, correct_result, teacher_id, driver_type, question_filename], f"QuestionID = '{question_id}'")
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/submit', methods=['POST'])
def submit_file():
    """Runs the primary number function and returns a response."""
    try:
        question_id = request.args.get('question_id')
        student_id = request.args.get('student_id')
        # array = request.args.get('array')
        request_data = request.data.decode("utf-8")
        print(question_id)
        print(student_id)
        # print(array)
        print(request_data)
        response = function_handler.submit(
            student_id, question_id, request_data)
        return jsonify(response)
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/cluster', methods=['GET'])
def cluster():
    # Get the question_id from the query parameter
    question_id = request.args.get('question_id')
    # Optional: Get the threshold from the query parameter, default to 2
    threshold = int(request.args.get('threshold', 2))

    if not question_id:
        return jsonify({"error": "Question ID is required"}), 400

    try:
        # Call the clustering function
        result = function_handler.clustering(question_id, threshold)
        # Since result is a JSON string, convert it to a Python dict for jsonify
        result_dict = json.loads(result)
        return jsonify(result_dict), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(threaded=True, port=5000, host="0.0.0.0", debug=True)
