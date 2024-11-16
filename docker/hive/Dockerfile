FROM openjdk:11-jdk-slim-buster

# Install required packages
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean

# Install Hadoop (valid URL for version 3.3.6)
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xzf hadoop-3.3.6.tar.gz -C /opt && \
    mv /opt/hadoop-3.3.6 /opt/hadoop && \
    rm hadoop-3.3.6.tar.gz

# Set Hadoop Environment Variables
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Install Hive (valid URL for version 2.3.8)
RUN wget https://archive.apache.org/dist/hive/hive-2.3.8/apache-hive-2.3.8-bin.tar.gz && \
    tar -xzf apache-hive-2.3.8-bin.tar.gz -C /opt && \
    mv /opt/apache-hive-2.3.8-bin /opt/hive && \
    rm apache-hive-2.3.8-bin.tar.gz

# Set Hive Environment Variables
ENV HIVE_HOME=/opt/hive
ENV PATH=$PATH:$HIVE_HOME/bin

# Copy Hive configuration
COPY conf/hive-site.xml /opt/hive/conf/hive-site.xml

# Add initialization script
COPY scripts/init_hive.sh /opt/init_hive.sh
RUN chmod +x /opt/init_hive.sh

# Run the Hive server
CMD ["/opt/init_hive.sh"]
