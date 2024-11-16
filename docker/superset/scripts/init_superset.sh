#!/bin/bash

# Initialize the database
superset db upgrade

# Initialize Superset
superset init

# Create an admin user if not already created
superset fab create-admin --username admin --firstname Admin --lastname User --email admin@superset.com --password admin

# Load examples (optional, comment out if not needed)
superset load-examples

# Start Superset using Gunicorn
gunicorn \
    -w 2 \
    -k gevent \
    --timeout 120 \
    -b 0.0.0.0:8088 \
    "superset.app:create_app()"