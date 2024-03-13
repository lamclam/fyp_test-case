import functools
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from utility import get_data, remove_if_exists
from primary_number import primary_number
from palindrome import palindrome
import json

app = Flask(__name__)
CORS(app)

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


@app.route('/primary_number', methods=['POST'])
@validate_request
def run_primary_number():
    """Runs the primary number function and returns a response."""
    try:
        request_data = request.data.decode('utf-8')
        response, temp_file_name = primary_number(request_data)
        remove_if_exists(temp_file_name)
        remove_if_exists(temp_file_name[:-5] + CLASS_EXTENSION)
        return jsonify(response)
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/palindrome', methods=['POST'])
@validate_request
def run_palindrome():
    """Runs the palindrome function and returns a response."""
    try:
        request_data = request.data.decode('utf-8')
        response, test_file_name, code_file_name = palindrome(request_data)
        remove_if_exists(test_file_name)
        remove_if_exists(test_file_name[:-5] + CLASS_EXTENSION)
        remove_if_exists(code_file_name)
        remove_if_exists(code_file_name[:-5] + CLASS_EXTENSION)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({ERROR_KEY: str(e)}), 400


@app.route('/getdata', methods=['GET'])
def getdata():
    """Returns the data from a specified table."""
    try:
        table_name = request.args.get('table_name')
        column_name = request.args.get('column_name')
        where_clause = request.args.get('where_clause')
        data = get_data(table_name, column_name, where_clause)

        if data:
            return json.loads(data)
        else:
            return jsonify({ERROR_KEY: 'No data found'}), 404
    except Exception as e:
        return jsonify({ERROR_KEY: str(e)}), 400


if __name__ == '__main__':
    app.run(threaded=True, port=5000, host="0.0.0.0")
