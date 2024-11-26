from pymilvus import connections, FieldSchema, CollectionSchema, Collection
import json

MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
EMBEDDINGS_DIM = 384

def load_to_milvus(processed_file_path):
    # Connect to Milvus
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)

    # Define schema
    fields = [
        FieldSchema(name="id", dtype="INT64", is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype="FLOAT_VECTOR", dim=EMBEDDINGS_DIM),
    ]
    schema = CollectionSchema(fields, "Amazon Product Data")

    # Create collection
    collection = Collection(name="amazon_products", schema=schema)

    # Load processed data
    with open(processed_file_path, "r") as file:
        data = json.load(file)

    embeddings = [item["embedding"] for item in data]
    collection.insert([list(range(len(embeddings))), embeddings])
    print(f"Inserted {len(embeddings)} embeddings into Milvus.")
