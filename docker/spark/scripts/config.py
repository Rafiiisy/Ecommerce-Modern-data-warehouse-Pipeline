# config.py

# API Configuration
API_KEY = "7f65a16aa601423995fffdc8faa37087"
API_BASE_URL = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"

# Spark Configuration
SPARK_APP_NAME = "CurrencyExchangeStreaming"
SPARK_MASTER_URL = "spark://spark-master:7077"

# HDFS Configuration
HDFS_NAMENODE_URL = "hdfs://namenode:9820"
HDFS_OUTPUT_PATH = "/user/spark/exchange_rates"  # Adjust the output path as needed

# Logging Configuration
LOG_FILE = "logs/currency_streaming.log"

# Currency pairs to monitor
CURRENCY_PAIRS = [
    "EUR",
    "GBP",
    "JPY",
    "AUD",
    "CAD",
    "IDR",  # Indonesian Rupiah
    "SGD",  # Singapore Dollar
    "MYR"   # Malaysian Ringgit
]

# Spark Streaming Configuration
STREAMING_CONFIG = {
    "rowsPerSecond": 1,
    "format": "rate"
}

# Data Processing
BATCH_SIZE = 100
MAX_OFFSETS_PER_TRIGGER = 200

# Error Handling
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
