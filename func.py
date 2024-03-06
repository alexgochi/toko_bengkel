import psycopg2


def select_req(query, param={}):
    # Database connection parameters
    host = '127.0.0.1'
    port = '5400'
    database = 'postgres'
    user = 'postgres'
    password = 'admin'

    try:
        # Connect to the database
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
            connect_timeout=1
        )
        # # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # # Execute SQL queries
        cursor.execute(f'''select json_agg(x) from ({query}) x''', param)
        data = cursor.fetchone()

        # # Close the cursor and connection
        cursor.close()
        connection.close()
        # return res
        return data[0]
    except Exception as e:
        return str(e)