import json
import mariadb

# Database connection details
host = "ip"
port = 3306
user = "fyp"
password = "pw"
database = "fyp"

# Function to retrieve data from a table


def get_data(table_name):
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

        # Execute the SELECT query on the specified table
        cursor.execute(f"SELECT * FROM {table_name}")

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
