import json
import mariadb

# Database connection details
host = "ip"
port = 3306
user = "fyp"
password = "password"
database = "fyp"


# Function to retrieve data from a table
def get_data_json(table_name, column_name=None, where_clause=None):
    # Check if table_name or column_name contains spaces
    if ' ' in table_name or (column_name is not None and ' ' in column_name):
        error = "Input should not contain spaces."
        raise ValueError(error)

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
        if not rows:  # Check if the result is empty
            return None  # Return None if no rows are found
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


# Function to retrieve data from a table
def get_single_data_value(table_name, column_name, where_clause, matcher):
    # Check if table_name or column_name contains spaces
    if ' ' in table_name or (column_name is not None and ' ' in column_name):
        error = "Input should not contain spaces."
        raise ValueError(error)

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

        # Formulate SQL query
        sql_query = f"SELECT {column_name} FROM {
            table_name} WHERE {where_clause} = \'{matcher}\'"

        # Execute the query
        cursor.execute(sql_query)

        # Fetch the first row of the result
        result = cursor.fetchone()

        # Check if the result is not None
        if result:
            value = result[0]  # Assuming the query returns one column
        else:
            value = None  # No result found

        # Convert the value to JSON format and return
        return value

    except mariadb.Error as e:
        # Handle any database errors and return an error message
        # error = {"error": str(e)}
        return str(e)

    finally:
        # Close the database connection in the finally block
        if conn:
            conn.close()


# Usage example:
# response = add_new_record("users", ["name", "email"], ["John Doe", "john@example.com"])
def add_new_record(table_name, columns, values):
    if ' ' in table_name:
        error = "Table name should not contain spaces."
        raise ValueError(error)

    # Ensure that columns and values are provided and are lists of the same length
    if not columns or not values or len(columns) != len(values):
        error = "Columns and values must be provided in equal numbers."
        return json.dumps({"error": error})

    try:
        # Establish database connection
        conn = mariadb.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Prepare the SQL query for insertion
        formatted_columns = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))
        sql_query = f"INSERT INTO {
            table_name} ({formatted_columns}) VALUES ({placeholders})"

        # Execute the INSERT query
        cursor.execute(sql_query, tuple(values))
        conn.commit()  # Commit the changes

        # Check if the insert was successful
        return json.dumps({"success": "Record added successfully."})

    except mariadb.Error as e:
        error = {"error": str(e)}
        return json.dumps(error)

    finally:
        if conn:
            conn.close()


# Example usage:
# response = update_record("users", ["email", "phone"], ["john@newdomain.com", "1234567890"], "name = 'John Doe'")
def update_record(table_name, columns, values, where_clause):
    if ' ' in table_name:
        error = "Table name should not contain spaces."
        raise ValueError(error)

    # Ensure that columns and values are provided and are lists of the same length
    if not columns or not values or len(columns) != len(values):
        error = "Columns and values must be provided in equal numbers."
        return json.dumps({"error": error})

    try:
        # Establish database connection
        conn = mariadb.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Prepare the SQL query for updating
        set_parts = [f"{col} = %s" for col in columns]
        set_clause = ", ".join(set_parts)
        sql_query = f"UPDATE {table_name} SET {
            set_clause} WHERE {where_clause}"

        # Execute the UPDATE query
        cursor.execute(sql_query, tuple(values))
        conn.commit()  # Commit the changes

        # Check if the update was successful
        return json.dumps({"success": "Record updated successfully."})

    except mariadb.Error as e:
        error = {"error": str(e)}
        return json.dumps(error)

    finally:
        if conn:
            conn.close()


# Example usage:
# response = update_record("users", ["email", "phone"], ["john@newdomain.com", "1234567890"], "name = 'John Doe'")
# print(response)
def update_data(table_name, set_clause, where_clause):
    if ' ' in table_name:
        error = "Input should not contain spaces."
        raise ValueError(error)

    try:
        # Establish database connection
        conn = mariadb.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Formulate the UPDATE SQL query
        sql_query = f"UPDATE {table_name} SET {
            set_clause} WHERE {where_clause}"
        # Execute the UPDATE query
        cursor.execute(sql_query)
        conn.commit()  # Commit the changes

        # Check if the update was successful
        return json.dumps({"success": "Record updated successfully."})

    except mariadb.Error as e:
        error = {"error": str(e)}
        return json.dumps(error)

    finally:
        if conn:
            conn.close()


def delete_data(table_name, where_clause):
    if ' ' in table_name:
        error = "Input should not contain spaces."
        raise ValueError(error)

    try:
        # Establish database connection
        conn = mariadb.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Formulate the DELETE SQL query
        sql_query = f"DELETE FROM {table_name} WHERE {where_clause}"

        # Execute the DELETE query
        cursor.execute(sql_query)
        conn.commit()  # Commit the changes

        # Check if the delete was successful
        return json.dumps({"success": "Record deleted successfully."})

    except mariadb.Error as e:
        error = {"error": str(e)}
        return json.dumps(error)

    finally:
        if conn:
            conn.close()
