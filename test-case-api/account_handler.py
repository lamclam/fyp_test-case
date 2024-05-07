import json
import database_handler


def login(user_id, password):
    # Retrieve student data from the database using the user ID
    student_data = database_handler.get_data_json(
        'Students', None, f'StudentID = \"{user_id}\"')
    # Retrieve teacher data from the database using the user ID
    teacher_data = database_handler.get_data_json(
        'Teachers', None, f'TeacherID = \"{user_id}\"')
    user_type = ""

    # Determine if the user is a student or a teacher based on the data retrieved
    if student_data and not teacher_data:
        user_type = 'student'
    elif not student_data and teacher_data:
        user_type = 'teacher'
    else:
        # User ID does not match any record
        return {'error': 'The user id is not correct'}

    # Parse the JSON data of the user
    if user_type == 'student':
        user_data = json.loads(student_data)
    else:
        user_data = json.loads(teacher_data)

    # Debugging print statements
    print(user_data)
    print(user_data[0]['Password'])

    # Validate the provided password against the stored password
    if user_data[0]['Password'] == password:
        response = {'login': True,
                    'userName': user_data[0]['Name'],
                    'type': user_type
                    }
        return response
    else:
        raise ValueError("The user ID or password is not correct")


def update_user(user_id, user_type, user_name, user_password):
    # Ensure the user name is provided
    if not user_name:
        raise ValueError("User name must be provided")

    # Select the appropriate database table and column based on the user type
    if user_type == 'student':
        table_name = 'Students'
        id_column = 'StudentID'
    elif user_type == 'teacher':
        table_name = 'Teachers'
        id_column = 'TeacherID'
    else:
        raise ValueError('Invalid user type')

    # Construct the SQL update string
    update_string = f'Name = \"{user_name}\"'
    if user_password:
        update_string += f', Password = \"{user_password}\"'

    # Execute the update query
    try:
        print(table_name)
        print(update_string)
        print(f'{id_column} = \"{user_id}\"')
        response = database_handler.update_data(
            table_name, update_string, f'{id_column} = \"{user_id}\"')
        return {'updated':  response}
    except Exception as e:
        # Handle exceptions that occur during the update
        raise Exception("Failed to update data:", e)


def delete_user(user_id, user_type):
    # Ensure the user ID is provided
    if not user_id:
        raise ValueError("User ID must be provided")

    # Select the appropriate database table and column based on the user type
    if user_type == 'student':
        table_name = 'Students'
        id_column = 'StudentID'
    elif user_type == 'teacher':
        table_name = 'Teachers'
        id_column = 'TeacherID'
    else:
        raise ValueError('Invalid user type')

    # Execute the delete query
    try:
        database_handler.delete_data(
            table_name, f'{id_column} = \"{user_id}\"')
        return {'deleted': f'{id_column} = {user_id}'}
    except Exception as e:
        # Handle exceptions that occur during deletion
        raise Exception("Failed to delete data:", e)
