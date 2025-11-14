thonpython
import json
import logging
import sys
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup

from extractors.reviews_parser import parse_reviews
from extractors.complaints_parser import parse_complaints
from outputs.exporters import save_json

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def load_urls(file_path: str) -> List[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Failed to read URL file: {e}")
        sys.exit(1)

def fetch_page(url: str) -> BeautifulSoup:
    logging.info(f"Fetching: {url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        logging.error(f"Error fetching URL: {url} | {e}")
        return None

def detect_type(url: str) -> str:
    if "/customer-reviews" in url:
        return "review"
    if "/complaints" in url:
        return "complaint"
    return "unknown"

def main():
    if len(sys.argv) < 3:
        print("Usage: python src/runner.py <input_urls.txt> <output.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    urls = load_urls(input_file)
    results = []

    for url in urls:
        page_type = detect_type(url)
        soup = fetch_page(url)
        if not soup:
            continue

        if page_type == "review":
            parsed = parse_reviews(soup, url)
        elif page_type == "complaint":
            parsed = parse_complaints(soup, url)
        else:
            logging.warning(f"Skipping unknown URL type: {url}")
            continue

        results.extend(parsed)

    save_json(results, output_file)
    logging.info(f"Saved output to {output_file}")

if __name__ == "__main__":
    main()