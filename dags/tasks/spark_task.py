from pyspark.sql import SparkSession
import json
import os
from sentence_transformers import SentenceTransformer

PROCESSED_DATA_PATH = "./data/processed"


def process_data(raw_file_path):
    # Initialize Spark
    spark = SparkSession.builder.appName("AmazonDataProcessing").getOrCreate()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load raw data
    raw_df = spark.read.json(raw_file_path)

    # Transform and filter data
    raw_rdd = raw_df.rdd.map(lambda row: {
        "title": row["title"],
        "price": row["price"],
        "rating": row["rating"],
        "embedding": model.encode(row["title"]).tolist() if row["title"] else None
    }).filter(lambda x: x["embedding"] is not None)

    # Save processed data
    processed_data_path = os.path.join(PROCESSED_DATA_PATH, "processed_data.json")
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    with open(processed_data_path, "w") as file:
        json.dump(raw_rdd.collect(), file, indent=4)

    print("Processed data saved.")
    return processed_data_path
