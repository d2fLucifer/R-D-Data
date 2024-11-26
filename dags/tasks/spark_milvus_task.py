from pymilvus import connections, utility
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Milvus server connection settings
milvus_host = "localhost"  # Replace with your Milvus host
milvus_port = "19530"  # Replace with your Milvus port


def check_milvus_connection():
    try:
        # Try connecting to the Milvus server
        connections.connect(alias="default", host=milvus_host, port=milvus_port)

        # Check if the server is alive
        is_alive = utility.has_collection("product_embeddings")  # Change collection name if needed
        if is_alive:
            logging.info(f"Successfully connected to Milvus server at {milvus_host}:{milvus_port}.")
        else:
            logging.warning(f"Milvus server is up but the collection does not exist.")

        # Optionally, check other server info
        server_info = utility.get_server_version()
        logging.info(f"Milvus server version: {server_info}")

    except Exception as e:
        logging.error(f"Failed to connect to Milvus server: {e}")
        return False
    return True


if __name__ == "__main__":
    if check_milvus_connection():
        logging.info("Milvus connection is successful.")
    else:
        logging.error("Milvus connection failed.")
