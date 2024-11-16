# config.py

# Spark Configuration
SPARK_APP_NAME = "SalesPredictionTraining"
SPARK_MASTER_URL = "local[*]"  # Adjust if running on a cluster
HDFS_NAMENODE_URL = "hdfs://namenode:9820"

# Paths
HDFS_INPUT_PATH = "/user/nifi/data/finalData_default_1.csv"  # Path to the dataset in HDFS
HDFS_OUTPUT_PATH = "/user/nifi/sales_model"  # Path to save the trained model

# Data Preprocessing
FEATURE_COLUMNS = [
    "orderDateId",
    "requiredDateId",
    "shippedDateId",
    "quantityOrdered",
    "priceEach",
]
LABEL_COLUMN = "priceEach"  # Change if you're predicting a different column

# Train-Test Split
TRAIN_TEST_SPLIT = [0.8, 0.2]

# Logging Configuration
LOG_FILE = "logs/train_model.log"
