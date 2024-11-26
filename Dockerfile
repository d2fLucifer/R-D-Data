# Start with the official Airflow image as the base
FROM apache/airflow:2.9.2

# Switch to root to install additional packages
USER root

# Install Spark and related dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk-headless \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Java environment variables required by Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Spark binaries
ENV SPARK_VERSION=3.4.1
RUN curl -fsSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz | tar -xz -C /opt \
    && mv /opt/spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Install Python packages for Airflow and Spark integration
RUN pip install --no-cache-dir pyspark==${SPARK_VERSION} \
    apache-airflow-providers-apache-spark

# Create directories for Spark and Airflow logs
RUN mkdir -p /opt/airflow/logs /opt/bitnami/spark/app

# Set permissions for airflow user
RUN chown -R airflow: /opt/airflow /opt/spark

# Switch back to the airflow user
USER airflow

# Define the entrypoint for the container
ENTRYPOINT ["/entrypoint"]

# Set default command
CMD ["webserver"]
