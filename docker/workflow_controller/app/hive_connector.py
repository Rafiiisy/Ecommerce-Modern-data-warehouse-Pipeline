# hive_connector.py

from pyhive import hive
from pyhive.exc import DatabaseError
import config
import logging

logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class HiveConnector:
    def __init__(self):
        """Initialize Hive connection."""
        self.host = config.HIVE_HOST
        self.port = config.HIVE_PORT
        self.database = config.HIVE_DATABASE
        self.connection = None

    def connect(self):
        """Establish a connection to the Hive server."""
        try:
            logging.info("Connecting to Hive...")
            self.connection = hive.Connection(
                host=self.host,
                port=self.port,
                database=self.database,
                username="hive"
            )
            logging.info("Connected to Hive successfully.")
        except DatabaseError as e:
            logging.error(f"Error connecting to Hive: {e}")
            raise

    def create_external_table(self, table_name, schema, hdfs_location):
        try:
            cursor = self.connection.cursor()
            columns = ",\n".join([f"{col_name} {data_type}" for col_name, data_type in schema])
            query = f"""
            CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
                {columns}
            )
            STORED AS PARQUET
            LOCATION '{hdfs_location}'
            """
            logging.info(f"Executing query to create table {table_name}:\n{query}")
            cursor.execute(query)
            logging.info(f"Table {table_name} created successfully.")
        except Exception as e:
            logging.error(f"Error creating table {table_name}: {e}")
            raise


    def fetch_data(self, query):
        """
        Fetch data from Hive using a SQL query.

        :param query: The SQL query to execute
        :return: Fetched data as a list of tuples
        """
        try:
            cursor = self.connection.cursor()
            logging.info(f"Executing query: {query}")
            cursor.execute(query)
            result = cursor.fetchall()
            logging.info(f"Query executed successfully. Rows fetched: {len(result)}")
            return result
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise

    def close(self):
        """Close the Hive connection."""
        if self.connection:
            self.connection.close()
            logging.info("Hive connection closed.")
