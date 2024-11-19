FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    procps \
    python3-dev \
    libffi-dev \
    libsasl2-dev \
    openjdk-17-jre-headless \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Dynamically determine JAVA_HOME
RUN export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java)))) && \
    echo "JAVA_HOME=$JAVA_HOME" && \
    ls -l $JAVA_HOME/bin && \
    echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment

# Set the correct JAVA_HOME for the ARM64 architecture
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Verify Java installation
RUN java -version && echo "JAVA_HOME=$JAVA_HOME" && ls -l $JAVA_HOME/bin/java

# Copy Python dependencies
COPY app/requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ /app/

# Expose the port
EXPOSE 8080

# Set the entry point
CMD ["python", "controller.py"]
