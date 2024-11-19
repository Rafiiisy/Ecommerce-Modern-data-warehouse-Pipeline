import requests
import json
import time
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions import current_timestamp, lit
import config

def fetch_exchange_rates():
    url = f"https://openexchangerates.org/api/latest.json?app_id={config.API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    return response.json()

def transform_to_dataframe(spark, data):
    rates = data.get("rates", {})
    base_currency = data.get("base", "USD")
    timestamp = data.get("timestamp", None)

    # Define schema
    schema = StructType([
        StructField("currency", StringType(), True),
        StructField("rate", DoubleType(), True),
        StructField("base_currency", StringType(), True),
        StructField("api_timestamp", TimestampType(), True),
        StructField("ingest_timestamp", TimestampType(), True),
    ])

    # Convert UNIX timestamp to readable timestamp
    from datetime import datetime
    api_timestamp = datetime.utcfromtimestamp(timestamp)

    # Get current timestamp for ingestion time
    ingest_timestamp = datetime.utcnow()

    # Filter for specific currencies if needed
    if config.CURRENCY_PAIRS:
        rates = {k: v for k, v in rates.items() if k in config.CURRENCY_PAIRS}

    # Transform rates dictionary into a list of rows
    rows = [
        (
            currency,
            float(rate),
            base_currency,
            api_timestamp,
            ingest_timestamp
        )
        for currency, rate in rates.items()
    ]

    # Create Spark DataFrame
    return spark.createDataFrame(rows, schema=schema)

def write_to_hdfs(dataframe, hdfs_path):
    # Append data to existing dataset
    dataframe.write.mode("append").parquet(hdfs_path)

def main():
    # Create Spark Session
    spark = SparkSession.builder \
        .appName("OpenExchangeIngestion") \
        .config("spark.hadoop.fs.defaultFS", config.HDFS_NAMENODE_URL) \
        .getOrCreate()

    try:
        while True:
            # Step 1: Fetch Data
            exchange_data = fetch_exchange_rates()

            # Step 2: Transform to DataFrame
            df = transform_to_dataframe(spark, exchange_data)

            # Step 3: Write to HDFS
            hdfs_path = config.HDFS_OUTPUT_PATH
            write_to_hdfs(df, hdfs_path)

            print(f"Data successfully written to HDFS at {hdfs_path}")

            # Sleep for the specified interval
            print(f"Sleeping for {config.FETCH_INTERVAL} seconds...")
            time.sleep(config.FETCH_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping data ingestion.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
