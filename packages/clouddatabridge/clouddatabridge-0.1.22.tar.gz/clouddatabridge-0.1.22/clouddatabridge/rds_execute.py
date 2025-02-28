import pymysql.cursors
import pymysql
from .db_connection import get_db_connection

# Global dictionary to store connections
GLOBAL_CONNECTIONS = {}

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

    finally:
        if connection:
            connection_obj.close_connection()

def get_global_connection(service, config):
    """
    Retrieves an existing database connection from the global store.
    If a connection does not exist or is closed, a new one is created and stored.
    """
    # Check if a valid connection already exists
    if service in GLOBAL_CONNECTIONS:
        connection_obj = GLOBAL_CONNECTIONS[service]
        if connection_obj and connection_obj.db_connection and connection_obj.db_connection.open:
            print(f"Reusing existing database connection for {service}.")
            return connection_obj
        else:
            print(f"Connection for {service} is closed. Re-establishing...")

    # No valid connection exists, create a new one
    print(f"Creating a new database connection for {service}.")
    GLOBAL_CONNECTIONS[service] = get_db_connection(service, **config)

    # Ensure the connection is valid before returning
    if not GLOBAL_CONNECTIONS[service] or not GLOBAL_CONNECTIONS[service].db_connection or not GLOBAL_CONNECTIONS[service].db_connection.open:
        raise ValueError(f"Failed to establish a valid database connection for {service}.")

    return GLOBAL_CONNECTIONS[service]


def rds_execute_with_connection(query, params=None, batch_size=1, connection_obj=None):
    """
    Executes an SQL query using an existing database connection.
    If no connection is provided, attempts to fetch from the global store.
    """
    if not connection_obj or not connection_obj.db_connection or not connection_obj.db_connection.open:
        print("No valid connection provided, trying to fetch from global connections.")
        if GLOBAL_CONNECTIONS:
            connection_obj = next(iter(GLOBAL_CONNECTIONS.values()))  # Get first available connection
        if not connection_obj or not connection_obj.db_connection or not connection_obj.db_connection.open:
            raise ValueError("No valid database connection available.")

    connection = connection_obj.db_connection

    try:
        with connection.cursor() as cursor:
            if isinstance(params, list) and all(isinstance(i, (tuple, list)) for i in params):
                if batch_size > 1:
                    for batch in chunked_data(params, batch_size):
                        cursor.executemany(query, batch)
                else:
                    cursor.executemany(query, params)
            else:
                cursor.execute(query, params) if params else cursor.execute(query)

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