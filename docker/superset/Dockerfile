# Dockerfile for Superset
FROM apache/superset:latest

# Add initialization script
COPY scripts/init_superset.sh /app/init_superset.sh

RUN pip install gevent


# Expose Superset port
EXPOSE 8088

# Run the initialization script
ENTRYPOINT ["/app/init_superset.sh"]
