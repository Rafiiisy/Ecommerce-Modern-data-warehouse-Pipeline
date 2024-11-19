# model_trainer.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
import config
import logging

logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ModelTrainer:
    def __init__(self, spark_session):
        """Initialize with the given Spark session."""
        self.spark = spark_session
        logging.info("ModelTrainer initialized with existing Spark session.")

    def load_data(self, input_path):
        """Load data from HDFS."""
        try:
            logging.info(f"Loading data from HDFS path: {input_path}")
            data = self.spark.read.parquet(input_path)
            logging.info("Data loaded successfully.")
            return data
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise

    def preprocess_data(self, data):
        """Preprocess the data for training."""
        try:
            logging.info("Preprocessing data...")
            # Drop rows with NULL values in feature columns
            data = data.dropna(subset=config.FEATURE_COLUMNS)
            # Assemble features
            assembler = VectorAssembler(inputCols=config.FEATURE_COLUMNS, outputCol="features")
            data = assembler.transform(data)
            logging.info("Data preprocessing completed.")
            return data
        except Exception as e:
            logging.error(f"Error during preprocessing: {e}", exc_info=True)
            raise

    def train_model(self, data):
        """Train the regression model."""
        try:
            logging.info("Splitting data into training and test sets...")
            train, test = data.randomSplit(config.TRAIN_TEST_SPLIT, seed=42)
            logging.info("Training the model...")
            lr = LinearRegression(featuresCol="features", labelCol="total_sales")
            model = lr.fit(train)
            logging.info("Evaluating the model...")
            predictions = model.transform(test)
            evaluator = RegressionEvaluator(labelCol="total_sales", predictionCol="prediction", metricName="rmse")
            rmse = evaluator.evaluate(predictions)
            logging.info(f"Model evaluation completed. RMSE: {rmse}")
            return model
        except Exception as e:
            logging.error(f"Error during model training: {e}")
            raise

    def save_model(self, model, output_path):
        """Save the trained model to HDFS."""
        try:
            logging.info(f"Saving the model to HDFS path: {output_path}")
            model.write().overwrite().save(output_path)
            logging.info("Model saved successfully.")
        except Exception as e:
            logging.error(f"Error saving the model: {e}")
            raise

    def stop_spark(self):
        """Stop the Spark session."""
        self.spark.stop()
        logging.info("Spark session stopped.")
