from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.types import IntegerType
from datetime import datetime
from functools import reduce
import time

def forecast_currency(spark, currency_df, min_date, currency):
    """
    Train a Linear Regression model and forecast the next 30 days for the given currency.
    """
    # Assemble features for the model
    assembler = VectorAssembler(inputCols=["days_since_start"], outputCol="features")
    currency_df = assembler.transform(currency_df).select("features", F.col("rate").alias("label"), "days_since_start")
    
    # Train Linear Regression model
    lr = LinearRegression(featuresCol="features", labelCol="label")
    model = lr.fit(currency_df)
    
    # Generate future dates for forecasting
    max_days = int(currency_df.agg(F.max("days_since_start")).collect()[0][0])  # Ensure max_days is an integer
    future_dates = [(int(max_days) + i) for i in range(1, 31)]  # Ensure each element is an integer
    future_df = spark.createDataFrame(future_dates, IntegerType()).toDF("days_since_start")
    
    # Retain days_since_start before transformation
    future_df = future_df.withColumn("days_since_start", F.col("days_since_start").cast(IntegerType()))
    future_df = assembler.transform(future_df).select("features", "days_since_start")
    
    # Predict future rates
    forecast = model.transform(future_df)
    forecast = forecast.withColumn("date", F.expr(f"date_add('{min_date}', days_since_start)"))
    
    # Use the passed currency value
    return forecast.select("date", F.lit(currency).alias("currency"), F.col("prediction").alias("forecasted_rate"))

def main():
    # Initialize Spark session
    spark = SparkSession.builder.appName("ExchangeRateForecast").getOrCreate()

    # Infinite loop for running the process every 24 hours
    while True:
        # Define HDFS base path
        base_hdfs_path = "hdfs://namenode:9820/user/spark/exchange-rates"

        # Get current date to dynamically set file path for each hour's file
        current_date = datetime.now().strftime('%Y-%m-%d')
        hdfs_input_path = f"{base_hdfs_path}/{current_date}/*"
        hdfs_output_path = f"hdfs://namenode:9820/user/spark/forecast_output/{current_date}/forecast.parquet"

        # Load the data
        df = spark.read.parquet(hdfs_input_path)

        # Ensure columns are in the expected format
        df = df.select("currency", "rate", "timestamp", "date")
        
        # Convert 'date' column to a numeric format (days since first date) for forecasting
        min_date = df.agg(F.min("date")).collect()[0][0]
        df = df.withColumn("days_since_start", F.datediff(F.col("date"), F.lit(min_date)).cast(IntegerType()))


        # Get a list of unique currencies
        currencies = df.select("currency").distinct().rdd.flatMap(lambda x: x).collect()

        # List to hold forecast DataFrames for each currency
        forecasts = []

        # Process each currency individually
        for currency in currencies:
            currency_df = df.filter(F.col("currency") == currency)
            forecast_df = forecast_currency(spark, currency_df, min_date, currency)
            forecasts.append(forecast_df)

        # Union all currency forecasts and save to HDFS
        if forecasts:
            forecast_result = reduce(lambda df1, df2: df1.unionAll(df2), forecasts)
            forecast_result.write.mode("overwrite").parquet(hdfs_output_path)
            print(f"Forecast data saved to {hdfs_output_path}")
        else:
            print("No forecast data generated.")

        # Wait for 24 hours before the next iteration
        print("Waiting for 24 hours before the next forecast...")
        time.sleep(86400)

if __name__ == "__main__":
    main()
