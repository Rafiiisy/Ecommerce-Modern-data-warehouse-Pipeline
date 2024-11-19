# controller.py

from pyspark.sql import SparkSession
from notifications import NotificationManager
from hive_connector import HiveConnector
from spark_preprocessor import SparkPreprocessor
from model_trainer import ModelTrainer
import config

class WorkflowController:
    def __init__(self):
        """Initialize all components."""
        self.notification_manager = NotificationManager()
        self.hive_connector = HiveConnector()
        self.spark_session = SparkSession.builder \
            .appName(config.SPARK_APP_NAME) \
            .config("spark.hadoop.fs.defaultFS", config.HDFS_NAMENODE_URL) \
            .getOrCreate()
        self.spark_preprocessor = SparkPreprocessor(self.spark_session)
        self.model_trainer = ModelTrainer(self.spark_session)

    def check_hdfs_data_availability(self):
        """Check if the required data exists in HDFS."""
        self.notification_manager.print_message("Checking HDFS for required data...")
        try:
            data_exists = self.spark_session._jvm.org.apache.hadoop.fs.FileSystem \
                .get(self.spark_session._jsc.hadoopConfiguration()) \
                .exists(self.spark_session._jvm.org.apache.hadoop.fs.Path(config.HDFS_INPUT_PATH))
            if not data_exists:
                self.notification_manager.print_message(
                    f"Required data not found at {config.HDFS_INPUT_PATH}.", "ERROR"
                )
                return False
            self.notification_manager.print_message("Required data is available in HDFS.")
            return True
        except Exception as e:
            self.notification_manager.print_message(f"Error checking HDFS data: {e}", "ERROR")
            return False

    def preprocess_data(self):
        """Run Spark-based preprocessing."""
        self.notification_manager.print_message("Starting preprocessing workflow...")
        try:
            # Load and preprocess data
            raw_data = self.spark_preprocessor.load_data(config.HDFS_INPUT_PATH)
            exchange_rate_data = self.spark_preprocessor.load_exchange_rate_data(config.EXCHANGE_RATES_PATH)
            preprocessed_data = self.spark_preprocessor.preprocess_data(raw_data, exchange_rate_data)
            self.spark_preprocessor.save_to_hdfs(preprocessed_data, config.HDFS_PREPROCESSED_PATH)
        except Exception as e:
            self.notification_manager.print_message(f"Error during preprocessing workflow: {e}", "ERROR")

    def create_hive_table(self):
        """Create or update the Hive table."""
        self.notification_manager.print_message("Creating Hive table for preprocessed data...")
        try:
            self.hive_connector.connect()
            self.hive_connector.create_external_table(
                table_name=config.HIVE_TABLE,
                schema=config.HIVE_TABLE_SCHEMA,
                hdfs_location=config.HDFS_PREPROCESSED_PATH
            )
            self.notification_manager.print_message("Hive table created successfully.")
        except Exception as e:
            self.notification_manager.print_message(f"Error creating Hive table: {e}", "ERROR")
        finally:
            self.hive_connector.close()

    def train_model(self):
        """Train a machine learning model."""
        self.notification_manager.print_message("Starting model training...")
        try:
            data = self.model_trainer.load_data(config.HDFS_PREPROCESSED_PATH)
            preprocessed_data = self.model_trainer.preprocess_data(data)
            model = self.model_trainer.train_model(preprocessed_data)
            self.model_trainer.save_model(model, config.MODEL_OUTPUT_PATH)
        except Exception as e:
            self.notification_manager.print_message(f"Error during model training: {e}", "ERROR")

    def run(self):
        """Main workflow execution."""
        self.notification_manager.print_message("Initializing workflow controller...")
        if not self.check_hdfs_data_availability():
            self.notification_manager.print_message("Aborting workflow due to missing data.", "ERROR")
            return

        self.preprocess_data()
        self.create_hive_table()
        self.train_model()

        self.spark_session.stop()
        self.notification_manager.print_message("Workflow completed successfully.")

if __name__ == "__main__":
    controller = WorkflowController()
    controller.run()
