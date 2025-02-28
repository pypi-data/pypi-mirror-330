import pymysql
import boto3
import time

class AWSRDSConnection:
    def __init__(self, host, user, password, database, region, port=3306, is_proxy=False):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.region = region
        self.port = port
        self.is_proxy = bool(is_proxy)
        self.db_connection = None

    def create_connection_token(self):
        client = boto3.client('rds', region_name=self.region)
        return client.generate_db_auth_token(
            DBHostname=self.host,
            Port=self.port,
            DBUsername=self.user,
            Region=self.region
        )

    def get_db_connection(self, max_retries=5, retry_delay=5):
        print(f"Inside AWSRDSConnection.get_db_connection() -> is_proxy: {self.is_proxy}, type: {type(self.is_proxy)}")
        if self.db_connection and self.db_connection.open:
            print("Using existing database connection.")
            return self.db_connection

        print("No active connection found. Establishing a new one...")
        retries = 0
        password_token = self.create_connection_token() if self.is_proxy else self.password
        if not password_token:
            raise ValueError("Password token is missing or empty.")
        while retries < max_retries:
            try:
                self.db_connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=password_token,
                    db=self.database,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    ssl={"use": True}
                )
                return self.db_connection

            except pymysql.OperationalError as e:
                retries += 1
                print(f"OperationalError: {e}. Retrying {retries}/{max_retries}...")
                time.sleep(retry_delay)

        raise pymysql.OperationalError(f"Failed to connect to the database after {max_retries} retries.")  

    def close_connection(self):
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None
