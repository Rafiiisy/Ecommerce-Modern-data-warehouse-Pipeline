from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import requests
from datetime import datetime

def create_spark_session():
    return SparkSession.builder \
        .appName("ExchangeRateVerifier") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9820") \
        .getOrCreate()

def check_api_data():
    """Fetch current data from API"""
    print("\nChecking API Data:")
    url = "https://v6.exchangerate-api.com/v6/d859a94bdc40c124d4842d22/latest/USD"
    response = requests.get(url)
    data = response.json()
    print(f"API Response Status: {response.status_code}")
    print(f"Total currencies in API: {len(data['conversion_rates'])}")
    return data

def check_hdfs_data(spark):
    """Check data stored in HDFS"""
    try:
        print("\nChecking HDFS Data:")
        # Read from HDFS
        df = spark.read.parquet("/exchange_rates")
        
        # Get basic stats
        total_records = df.count()
        unique_dates = df.select("date").distinct().count()
        unique_currencies = df.select("currency").distinct().count()
        
        print(f"\nTotal records in HDFS: {total_records}")
        print(f"Unique dates: {unique_dates}")
        print(f"Unique currencies: {unique_currencies}")
        
        # Show latest data
        print("\nLatest Exchange Rates in HDFS:")
        df.orderBy(desc("timestamp")).select(
            "currency", "rate", "timestamp"
        ).show(5)
        
        return df
    except Exception as e:
        print(f"Error reading HDFS data: {e}")
        return None

def compare_data(api_data, hdfs_df):
    """Compare API data with HDFS data"""
    print("\nComparing API vs HDFS data:")
    
    if hdfs_df is None:
        print("No HDFS data available for comparison")
        return
        
    # Get latest rates from HDFS
    latest_rates = hdfs_df.orderBy(desc("timestamp")) \
        .dropDuplicates(["currency"]) \
        .collect()
    
    # Convert to dictionary for easy comparison
    hdfs_rates = {row.currency: row.rate for row in latest_rates}
    api_rates = api_data['conversion_rates']
    
    # Compare counts
    print(f"\nCurrencies in API: {len(api_rates)}")
    print(f"Currencies in HDFS: {len(hdfs_rates)}")
    
    # Compare some major currencies
    major_currencies = ['EUR', 'GBP', 'JPY', 'IDR', 'SGD']
    print("\nComparison for major currencies:")
    print("Currency | API Rate | HDFS Rate | Difference")
    print("-" * 50)
    
    for curr in major_currencies:
        api_rate = api_rates.get(curr, 0)
        hdfs_rate = hdfs_rates.get(curr, 0)
        diff = abs(api_rate - hdfs_rate) if api_rate and hdfs_rate else 0
        print(f"{curr:8} | {api_rate:8.4f} | {hdfs_rate:9.4f} | {diff:9.4f}")

def main():
    print(f"Starting Data Verification at {datetime.now()}")
    spark = create_spark_session()
    
    try:
        # Check API data
        api_data = check_api_data()
        
        # Check HDFS data
        hdfs_df = check_hdfs_data(spark)
        
        # Compare data
        compare_data(api_data, hdfs_df)
        
    except Exception as e:
        print(f"Error during verification: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()