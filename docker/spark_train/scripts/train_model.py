import config
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator


def main():
    # Step 1: Initialize Spark Session
    spark = SparkSession.builder \
        .appName(config.SPARK_APP_NAME) \
        .config("spark.hadoop.fs.defaultFS", config.HDFS_NAMENODE_URL) \
        .getOrCreate()

    # Step 2: Load data from HDFS
    print("Loading data from HDFS...")
    try:
        data = spark.read.csv(config.HDFS_INPUT_PATH, header=True, inferSchema=True)
        print("Data loaded successfully!")
    except Exception as e:
        print(f"Error loading data: {e}")
        spark.stop()
        return

    print("Schema of the dataset:")
    data.printSchema()

    # Step 3: Drop unnecessary columns
    print("Dropping unnecessary columns...")
    columns_to_drop = [
        "orderDateId", "requiredDateId", "shippedDateId",
        "productCode", "orderNumber", "orderLineNumber",
        "customerNumber", "employeeNumber", "officeCode"
    ]
    data = data.drop(*columns_to_drop)

    # Step 4: Feature Engineering
    print("Engineering features...")
    try:
        # Calculate derived feature: total_sales
        data = data.withColumn("total_sales", col("quantityOrdered") * col("priceEach"))

        # Encode the 'status' column
        status_indexer = StringIndexer(inputCol="status", outputCol="status_index")
        data = status_indexer.fit(data).transform(data)

        # Assemble features
        feature_columns = ["quantityOrdered", "priceEach", "status_index"]
        assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
        data = assembler.transform(data)

        print("Feature engineering completed.")
    except Exception as e:
        print(f"Error during feature engineering: {e}")
        spark.stop()
        return

    print("Sample data after preprocessing:")
    data.select("features", "total_sales").show(5)

    # Step 5: Split into training and test sets
    train, test = data.randomSplit(config.TRAIN_TEST_SPLIT, seed=42)

    # Step 6: Train the model
    print("Training the model...")
    try:
        lr = LinearRegression(featuresCol="features", labelCol="total_sales")
        model = lr.fit(train)
        print("Model training completed.")
    except Exception as e:
        print(f"Error during model training: {e}")
        spark.stop()
        return

    # Step 7: Evaluate the model
    print("Evaluating the model...")
    try:
        predictions = model.transform(test)
        evaluator = RegressionEvaluator(labelCol="total_sales", predictionCol="prediction", metricName="rmse")
        rmse = evaluator.evaluate(predictions)
        print(f"Root Mean Squared Error (RMSE): {rmse}")
    except Exception as e:
        print(f"Error during model evaluation: {e}")
        spark.stop()
        return

    # Step 8: Save the model to HDFS
    print("Saving the model to HDFS...")
    print("Saving the model to HDFS...")
    try:
        model.write().overwrite().save(config.HDFS_OUTPUT_PATH)
        print(f"Model saved successfully at {config.HDFS_OUTPUT_PATH}.")
    except Exception as e:
        print(f"Error saving the model: {e}")
        spark.stop()
        return

    # Stop the Spark session
    spark.stop()


if __name__ == "__main__":
    main()
