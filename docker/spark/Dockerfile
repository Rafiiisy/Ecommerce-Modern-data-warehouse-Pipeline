FROM bitnami/spark:3.4.1

# Set working directory
WORKDIR /app

# Copy configuration files
COPY conf/core-site.xml /opt/bitnami/spark/conf/core-site.xml
COPY conf/hdfs-site.xml /opt/bitnami/spark/conf/hdfs-site.xml

FROM bitnami/spark:3.4.1

# Set the working directory
WORKDIR /app

# Copy application code into the container
COPY scripts/ingest_data.py /app/
COPY scripts/requirements.txt /app/
COPY scripts/config.py /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt


# Command to run the ingestion script
CMD ["python", "/app/ingest_data.py"]
