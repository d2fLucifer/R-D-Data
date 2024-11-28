# Start with the official Airflow image as the base
FROM apache/airflow:2.9.2

# Switch to root to install additional system dependencies
USER root

# Install Spark and related system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk-headless \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Java environment variables required by Spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Spark binaries
ENV SPARK_VERSION=3.4.1
RUN curl -fsSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz | tar -xz -C /opt \
    && mv /opt/spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark \
    && rm -rf /opt/spark-${SPARK_VERSION}-bin-hadoop3.tgz  # Clean up tarball to save space

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH

# Install Python packages for Airflow and Spark integration
USER airflow

# Copy requirements.txt before running pip install
COPY requirements.txt /tmp/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir \
    pyspark==${SPARK_VERSION} \
    apache-airflow-providers-apache-spark \
    pymilvus \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# Switch to root to create necessary directories
USER root
RUN mkdir -p /opt/airflow/logs /opt/bitnami/spark/app && \
    chown -R airflow: /opt/airflow /opt/spark

# Switch back to airflow user for Airflow runtime
USER airflow

# Define the entrypoint for the container
ENTRYPOINT ["/entrypoint"]

# Set default command
CMD ["webserver"]
