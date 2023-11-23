from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import re
import tempfile
import threading
import json
from database_handler import get_data
from result_handler import check_result, predict_class, convert_result

app = Flask(__name__)
CORS(app)


@app.route('/run_code', methods=['POST'])
def run_code():
    # Get the Java code from the request body
    code = request.data.decode('utf-8')

    json_data = json.loads(get_data("prime_number_ans"))

    results = []
    result_array = []
    expected_array = []

    temp_file_name = ''

    # Create a temporary Java file
    with tempfile.NamedTemporaryFile(suffix='.java', delete=False, dir='.') as temp_file:
        # Change the class name in the code to match the file name
        class_name = re.search(r'class\s+(\w+)', code)
        if class_name:
            temp_file_name = os.path.basename(temp_file.name[:-5])
            code = code.replace(class_name.group(1), temp_file_name)

        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    # Compile the Java code
    compile_process = subprocess.run(
        ['javac', temp_file_name + '.java'], capture_output=True, text=True)

    if compile_process.returncode == 0:
        count = 0
        # Compilation successful, execute the code for each stdin input
        for data in json_data:
            stdin = str(data['num'])  # Read the 'num' value from the JSON
            expected = data['ans']  # Read the 'ans' value from the JSON
            expected_array.append(expected)

            execute_process = subprocess.run(
                ['java', temp_file_name], input=stdin, capture_output=True, text=True)

            # Prepare the result for the current stdin input
            result = {
                'stdin': stdin,
                'stdout': execute_process.stdout.strip(),
                'stderr': execute_process.stderr.strip(),
                'pass': check_result(execute_process.stdout.strip(), expected),
                'expected': expected
            }

            results.append(result)
            result_array.append(convert_result(execute_process.stdout.strip()))
            count += 1

        # Check if all the results match the expected values, if not, make a prediction
        if len(result_array) == count:
            if result_array != expected_array:
                predict = predict_class(result_array)
                response = {'results': results, 'prediction': int(predict[0])}
            else:
                response = {'results': results}
    else:
        # Compilation error, extract the error message from the stderr output
        error_message = compile_process.stderr.strip()
        response = {'error': 'Compilation error', 'message': error_message}

    # Remove the temporary file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    class_file_path = temp_file_path[:-5] + '.class'
    if os.path.exists(class_file_path):
        os.remove(class_file_path)

    return jsonify(response)


@app.route('/getdata', methods=['GET'])
def getdata():
    table_name = request.args.get('table_name')
    return json.loads(get_data(table_name))


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
