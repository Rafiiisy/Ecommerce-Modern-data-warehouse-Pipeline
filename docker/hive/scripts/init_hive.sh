#!/bin/bash

# Initialize Hive Metastore
$HIVE_HOME/bin/schematool -dbType postgres -initSchema

# Start Hive Metastore
$HIVE_HOME/bin/hive --service metastore &

# Wait for the Metastore to start
sleep 10

# Start HiveServer2
$HIVE_HOME/bin/hive --service hiveserver2