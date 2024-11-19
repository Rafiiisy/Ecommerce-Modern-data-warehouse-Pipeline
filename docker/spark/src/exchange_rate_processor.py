from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import requests
from datetime import datetime
import time

def create_spark_session():
    return SparkSession.builder \
        .appName("ExchangeRateETL") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9820") \
        .getOrCreate()

def fetch_exchange_rates():
    """Fetch exchange rate data from the API."""
    url = "https://openexchangerates.org/api/latest.json?app_id=cb24f865600248ad942811c72bbe3429&base=USD&symbols=IDR&prettyprint=false&show_alternative=false"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Extract relevant information
    rate = data["rates"]["IDR"]
    timestamp = data["timestamp"]
    return {"currency": "IDR", "rate": rate, "timestamp": timestamp}

def process_and_save_data(spark, data):
    """Process and save the exchange rate data to HDFS."""
    try:
        # Convert timestamp to datetime
        timestamp_dt = datetime.fromtimestamp(data['timestamp'])
        
        # Create a DataFrame row
        row = {
            'currency': data['currency'],
            'rate': float(data['rate']),
            'timestamp': timestamp_dt,
            'date': timestamp_dt.date()
        }
        
        # Define schema
        schema = StructType([
            StructField("currency", StringType(), True),
            StructField("rate", DoubleType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("date", DateType(), True)
        ])
        
        # Create DataFrame
        df = spark.createDataFrame([row], schema)
        
        # Display the data to be saved
        print("\nData to be saved to HDFS:")
        df.show()
        
        # Determine the HDFS path based on current date and time
        current_date = timestamp_dt.strftime('%Y-%m-%d')
        current_time = timestamp_dt.strftime('%H-%M-%S')
        output_path = f"hdfs://namenode:9820/user/spark/exchange-rates/{current_date}/{current_time}.parquet"

        
        # Save to HDFS in Parquet format
        df.write.mode("overwrite").parquet(output_path)
        print(f"Data saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"Error processing and saving data: {e}")
        return False

def main():
    print(f"Starting Exchange Rate ETL at {datetime.now()}")
    
    try:
        # Create Spark Session
        spark = create_spark_session()
        print("Spark session created successfully")
        
        while True:
            try:
                # Step 1: Fetch Data
                print("Fetching exchange rates...")
                data = fetch_exchange_rates()
                
                # Step 2: Process & Save Data
                print("Processing and saving data...")
                success = process_and_save_data(spark, data)
                
                if success:
                    print("ETL cycle completed successfully")
                else:
                    print("ETL cycle failed")
                
                # Wait for an hour before the next cycle
                wait_time = 3600  # 1 hour
                print(f"Waiting {wait_time} seconds before the next cycle...")
                time.sleep(wait_time)
                
            except Exception as e:
                print(f"Error in ETL cycle: {e}")
                print("Retrying in 5 minutes...")
                time.sleep(300)  # 5 minutes
                
    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        if 'spark' in locals():
            spark.stop()
            print("Spark session stopped")

if __name__ == "__main__":
    main()
