import requests
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import config

# Fetch Data from OpenExchange API
def fetch_exchange_rates():
    url = f"https://openexchangerates.org/api/latest.json?app_id={config.API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    return response.json()

# Transform Data into Spark DataFrame
def transform_to_dataframe(spark, data):
    rates = data.get("rates", {})
    base_currency = data.get("base", "USD")
    timestamp = data.get("timestamp", None)

    # Define schema
    schema = StructType([
        StructField("currency", StringType(), True),
        StructField("rate", DoubleType(), True),
        StructField("base_currency", StringType(), True),
        StructField("timestamp", StringType(), True),
    ])

    # Transform rates dictionary into a list of rows
    rows = [(currency, float(rate), base_currency, str(timestamp)) for currency, rate in rates.items()]

    # Create Spark DataFrame
    return spark.createDataFrame(rows, schema=schema)

# Write DataFrame to HDFS
def write_to_hdfs(dataframe, hdfs_path):
    dataframe.write.mode("overwrite").parquet(hdfs_path)

# Main function
def main():
    # Create Spark Session
    spark = SparkSession.builder \
        .appName("OpenExchangeIngestion") \
        .config("spark.hadoop.fs.defaultFS", config.HDFS_NAMENODE_URL) \
        .getOrCreate()

    try:
        # Step 1: Fetch Data
        exchange_data = fetch_exchange_rates()

        # Step 2: Transform to DataFrame
        df = transform_to_dataframe(spark, exchange_data)

        # Step 3: Write to HDFS
        hdfs_path = "/user/spark/exchange_rates"
        write_to_hdfs(df, hdfs_path)

        print(f"Data successfully written to HDFS at {hdfs_path}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
