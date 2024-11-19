# config.py

# HDFS Configuration
HDFS_NAMENODE_URL = "hdfs://namenode:9820"
HDFS_INPUT_PATH = "/user/nifi/data/finalData_default_1.csv"  # Input data path
HDFS_OUTPUT_PATH = "/user/nifi/data/preprocessed_data"  # Path to save processed data
HDFS_PREPROCESSED_PATH = "/user/nifi/data/preprocessed_data"


# Exchange Rate Data Path
EXCHANGE_RATES_PATH = "/user/nifi/exchange_rates"  # Path to exchange rate Parquet files

# Hive Configuration
HIVE_HOST = "hive-metastore"
HIVE_PORT = 10000
HIVE_DATABASE = "default"
HIVE_TABLE = "final_data"

HIVE_TABLE_SCHEMA = [
    ("productCode", "STRING"),
    ("orderNumber", "DOUBLE"),
    ("orderLineNumber", "DOUBLE"),
    ("customerNumber", "DOUBLE"),
    ("quantityOrdered", "DOUBLE"),
    ("priceEach", "DOUBLE"),
    ("order_date", "DATE"),
    ("currency", "STRING"),
    ("rate", "DOUBLE"),
    ("base_currency", "STRING"),
    ("adjusted_price", "DOUBLE"),
    ("total_sales", "DOUBLE")
]

PREPROCESS_DROP_COLUMNS = [
    "employeeNumber", "officeCode", "base_currency", "timestamp", "currency", "order_date", "date"
]

FEATURE_COLUMNS = ["quantityOrdered", "priceEach", "rate"]

# Spark Configuration
SPARK_APP_NAME = "WorkflowController"
SPARK_MASTER_URL = "local[*]"

# Model Training
TRAIN_TEST_SPLIT = [0.8, 0.2]
MODEL_OUTPUT_PATH = f"{HDFS_OUTPUT_PATH}/model"

# Notifications
NOTIFICATION_LOG_FILE = "/app/notifications.log"

# Logging
LOG_FILE = "/app/workflow.log"

# Visualization Integration (Superset)
SUPERSET_API_URL = "http://superset:8088/api/v1"
SUPERSET_AUTH_USERNAME = "admin"  # Superset admin username
SUPERSET_AUTH_PASSWORD = "admin"  # Superset admin password
SUPERSET_DATABASE_ID = 1  # Superset database ID linked to Hive (adjust as needed)

# Miscellaneous
ENABLE_HEALTH_CHECKS = True  # Enable or disable health checks
HEALTH_CHECK_ENDPOINTS = {
    "namenode": "http://namenode:9820",
    "hive-metastore": f"http://{HIVE_HOST}:{HIVE_PORT}",
    "superset": "http://superset:8088",
}
