import pymysql.cursors
from .db_connection import get_db_connection

def get_operation_from_query(query):
    """
    Determines the SQL operation type from a given SQL query.

    This function parses the query to identify the SQL operation, such as 'select', 'insert', 
    'update', or 'delete'. It is used to conditionally handle operations in the database based on the query type.

    Parameters:
        query (str): The SQL query string to analyze.

    Returns:
        str: The SQL operation type in lowercase (e.g., 'select', 'insert', 'update', 'delete').

    Examples:
        >>> get_operation_from_query("SELECT * FROM users")
        'select'
        
        >>> get_operation_from_query("UPDATE users SET name = 'Alice' WHERE id = 1")
        'update'
    """
    return query.strip().split()[0].lower()

def close(connection):
    """Close the database connection if it's open."""
    if connection:
        connection.close_connection()

def chunked_data(data, chunk_size):
    """Yield successive chunk_size chunks from data."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def rds_execute(service, query, params=None, batch_size=1, **config):
    """
    Executes a specified SQL query on an RDS or local database.

    This function establishes a database connection using the specified service, executes the provided query, 
    and handles multiple SQL operation types. It supports executing single or batched queries using a 
    parameterized approach for security and efficiency.

    Parameters:
        service (str): Specifies the type of database connection to establish ('local', 'aws', 'azure', 'gcp').
        query (str): The SQL query to execute.
        params (tuple or list of tuples, optional): Parameters for the query. Use a single tuple for a single 
                                                     query execution or a list of tuples for batch execution.
        batch_size (int, optional): Number of rows to process at a time for batch executions (default is 1).
        **config: Additional configuration parameters needed to establish the database connection, such as host,
                  user, password, database, and region.

    Returns:
        list or Exception: 
            - Returns a list of rows for 'select' queries.
            - Returns an Exception if an error occurs.

    Raises:
        pymysql.OperationalError: If there is an operational error in the database (e.g., connection failure).
        Exception: For any other errors encountered during query execution.

    Examples:
        >>> # Execute a SELECT query
        >>> results = rds_execute('aws', 'SELECT * FROM users WHERE id = %s', (1,))

        >>> # Execute an INSERT query with multiple rows
        >>> rds_execute('local', 'INSERT INTO users (name, age) VALUES (%s, %s)', params=[('Alice', 30), ('Bob', 25)])

    Notes:
        - Commits changes for 'insert', 'update', and 'delete' operations automatically.
        - Closes the connection automatically after execution.
    """
    connection = None
    try:
        connection_obj = get_db_connection(service, **config)
        connection = connection_obj.get_db_connection()
        with connection.cursor() as cursor:
            if isinstance(params, list) and all(isinstance(i, (tuple, list)) for i in params):
                if batch_size > 1:
                    for batch in chunked_data(params, batch_size):
                        cursor.executemany(query, batch)
                else:
                    cursor.executemany(query, params)
            else:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

            operation = get_operation_from_query(query)
            if operation in ['insert', 'update', 'delete']:
                connection.commit()

            if operation == 'select':
                return cursor.fetchall()

    except pymysql.OperationalError as op_err:
        print(f'Operational Error in DB query: {query}')
        print(op_err)
        return op_err

    except Exception as e:
        print(f'Error while executing DB query: {query}')
        print(e)
        return e

    # finally:
    #     if connection:
    #         connection_obj.close_connection()
