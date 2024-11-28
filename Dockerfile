# Use an official Airflow image as the base image
FROM apache/airflow:2.9.2

# Switch to root user to install system dependencies
USER root

# Install system dependencies (e.g., for Spark, Java, or other system packages)
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    python3-pip \
    curl \
    bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Ensure that the 'airflow' group and user exist (skip if they are already present)
RUN if ! getent group airflow; then groupadd -r airflow; fi && \
    if ! getent passwd airflow; then useradd -r -g airflow airflow; fi

# Copy the requirements.txt to the container
COPY requirements.txt /requirements.txt

# Switch to airflow user for running pip
USER airflow

# Install Python dependencies from the requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Switch back to root user to create necessary directories
USER root

# Create and set permissions for the directory where the data will be stored
RUN mkdir -p /opt/airflow/data && \
    chown -R airflow:airflow /opt/airflow/data && \
    chmod -R 775 /opt/airflow/data

# Switch back to airflow user for running Airflow services
USER airflow

# Set environment variables for Spark and Hadoop if necessary
ENV HADOOP_HOME=/opt/spark/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH

# Copy your DAGs, scripts, and other files to the Airflow container
COPY dags/ /opt/airflow/dags/
COPY data/ /opt/airflow/data/
