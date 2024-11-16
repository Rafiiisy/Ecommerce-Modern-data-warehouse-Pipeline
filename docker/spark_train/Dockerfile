FROM bitnami/spark:3.4.1

# Set the working directory
WORKDIR /app

# Copy application code
COPY scripts/train_model.py /app/
COPY scripts/requirements.txt /app/
COPY scripts/config.py /app/

# Copy Spark configuration
COPY conf/core-site.xml /opt/bitnami/spark/conf/core-site.xml
COPY conf/hdfs-site.xml /opt/bitnami/spark/conf/hdfs-site.xml

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the entrypoint to run the training script
CMD ["/opt/bitnami/spark/bin/spark-submit", "/app/train_model.py"]
