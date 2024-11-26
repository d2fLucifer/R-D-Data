import os
import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Directory to save scraped raw data
RAW_DATA_PATH = "./data/raw"

def scrape_amazon(amazon_url="https://www.amazon.com/s?k=technology"):
    """
    Scrapes product information from Amazon's search results page.

    Args:
        amazon_url (str): The URL of the Amazon search results page.

    Returns:
        str: Path to the saved JSON file containing product data.

    Raises:
        Exception: If the request fails after multiple retries.
    """
    os.makedirs(RAW_DATA_PATH, exist_ok=True)  # Ensure the data directory exists

    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.amazon.com/",
    }

    # Retry mechanism
    retries = 20
    response = None
    for attempt in range(retries):
        try:
            logging.info(f"Attempt {attempt + 1}: Fetching URL {amazon_url}")
            response = requests.get(amazon_url, headers=headers, timeout=10)
            if response.status_code == 200:
                break
            elif response.status_code in {503, 429}:  # Server errors or rate-limiting
                logging.warning(f"Received status {response.status_code}. Retrying...")
                time.sleep(random.uniform(5, 15))
            else:
                logging.error(f"Unexpected status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            time.sleep(random.uniform(2, 5))

    # Check final response
    if not response or response.status_code != 200:
        raise Exception(f"Failed to fetch data after {retries} retries.")

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    products = []

    # Extract product details
    for product in soup.select(".s-result-item"):
        title = product.select_one("h2 span").get_text(strip=True) if product.select_one("h2 span") else None
        price = product.select_one(".a-price .a-offscreen").get_text(strip=True) if product.select_one(".a-price .a-offscreen") else None
        rating = product.select_one(".a-icon-alt").get_text(strip=True) if product.select_one(".a-icon-alt") else None
        image_url = product.select_one("img.s-image")["src"] if product.select_one("img.s-image") else None
        description = product.select_one(".a-text-normal").get_text(strip=True) if product.select_one(".a-text-normal") else "No description available"

        if title:  # Add product only if the title is available
            products.append({
                "title": title,
                "price": price if price else "N/A",
                "rating": rating if rating else "N/A",
                "image_url": image_url if image_url else "N/A",
                "description": description
            })

    # Save extracted data to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file_path = os.path.join(RAW_DATA_PATH, f"raw_data_{timestamp}.json")
    with open(raw_file_path, "w") as file:
        json.dump(products, file, indent=4)

    logging.info(f"Scraped {len(products)} products. Data saved to {raw_file_path}.")
    return raw_file_path
