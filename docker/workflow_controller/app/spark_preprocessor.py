from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, to_date
from notifications import NotificationManager
import config

class SparkPreprocessor:
    def __init__(self, spark_session):
        """Initialize with the given Spark session."""
        self.spark = spark_session


    def load_data(self, input_path):
        """Load final data from HDFS."""
        NotificationManager.print_message(f"Loading data from HDFS path: {input_path}")
        try:
            data = self.spark.read.csv(input_path, header=True, inferSchema=True)
            NotificationManager.print_message("Final data loaded successfully.")
            # Inspect the data
            data.printSchema()
            data.show(5)
            return data
        except Exception as e:
            NotificationManager.print_message(f"Error loading final data: {e}", "ERROR")
            raise


    def load_exchange_rate_data(self, exchange_rate_path):
        """Load exchange rate data from HDFS."""
        NotificationManager.print_message(f"Loading exchange rate data from HDFS path: {exchange_rate_path}")
        try:
            exchange_rate_data = self.spark.read.parquet(exchange_rate_path)
            # Ensure timestamp is converted to date format for joining
            exchange_rate_data = exchange_rate_data.withColumn(
                "date", to_date(col("timestamp"))
            )
            exchange_rate_data.printSchema()
            exchange_rate_data.show(5)
            NotificationManager.print_message("Exchange rate data loaded successfully.")
            return exchange_rate_data
        except Exception as e:
            NotificationManager.print_message(f"Error loading exchange rate data: {e}", "ERROR")
            raise

    def preprocess_data(self, final_data):
        """Preprocess the data without date-based exchange rates."""
        NotificationManager.print_message("Starting data preprocessing...")
        try:
            # Set a default exchange rate
            default_rate = 1.0  # Replace with the appropriate rate if needed

            # Add the default exchange rate to the data
            final_data = final_data.withColumn("rate", lit(default_rate))

            # Calculate adjusted price and total sales
            final_data = final_data.withColumn(
                "adjusted_price", col("priceEach") * col("rate")
            ).withColumn(
                "total_sales", col("quantityOrdered") * col("adjusted_price")
            )

            # Drop unnecessary columns
            final_data = final_data.drop(*config.PREPROCESS_DROP_COLUMNS)

            NotificationManager.print_message("Data preprocessing completed successfully.")
            final_data.printSchema()
            final_data.show(5)
            return final_data
        except Exception as e:
            NotificationManager.print_message(f"Error during data preprocessing: {e}", "ERROR")
            raise


    def save_to_hdfs(self, data, output_path):
        """Save preprocessed data back to HDFS."""
        NotificationManager.print_message(f"Saving preprocessed data to HDFS path: {output_path}")
        try:
            data.write.mode("overwrite").parquet(output_path)
            NotificationManager.print_message(f"Data saved successfully to {output_path}")
        except Exception as e:
            NotificationManager.print_message(f"Error saving data to HDFS: {e}", "ERROR")
            raise

    def close(self):
        """Stop the Spark session."""
        self.spark.stop()
        NotificationManager.print_message("Spark session closed.")
