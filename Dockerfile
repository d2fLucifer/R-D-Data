# Base image for Spark
FROM bitnami/spark:latest

# Install necessary dependencies
USER root
RUN apt-get update && apt-get install -y python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add your requirements for PySpark if necessary
RUN pip3 install pyspark pandas

# Set work directory
WORKDIR /app

# Copy application code
COPY ./spark-app /app

# Expose Spark ports
EXPOSE 7077 8080

CMD ["/opt/bitnami/scripts/spark/run.sh"]
