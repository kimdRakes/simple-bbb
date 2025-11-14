thonpython
import logging
from bs4 import BeautifulSoup
from typing import List, Dict

def parse_complaints(soup: BeautifulSoup, base_url: str) -> List[Dict]:
    items = []

    complaints = soup.select(".complaint, .Complaint, .complaint-entry")
    if not complaints:
        logging.warning("No complaints found on page.")

    for c in complaints:
        try:
            category = c.select_one(".complaint-category, .category")
            category_text = category.get_text(strip=True) if category else None

            status = c.select_one(".complaint-status, .status")
            status_text = status.get_text(strip=True) if status else None

            complaint_type = c.select_one(".type, .complaint-type")
            complaint_type_text = complaint_type.get_text(strip=True) if complaint_type else "Complaint"

            date = c.select_one(".date, time")
            date_text = date.get_text(strip=True) if date else None

            details = c.select_one(".description, .content, .complaint-text")
            details_text = details.get_text(strip=True) if details else None

            source = c.select_one("a")
            source_url = source["href"] if source and source.has_attr("href") else base_url

            responses = {}
            business_response = c.select_one(".response-business, .business-response")
            consumer_response = c.select_one(".response-consumer, .consumer-response")

            if business_response:
                responses["business"] = business_response.get_text(strip=True)
            if consumer_response:
                responses["consumer"] = consumer_response.get_text(strip=True)

            items.append(
                {
                    "category": category_text,
                    "user": None,
                    "status": status_text,
                    "type": complaint_type_text,
                    "stars": None,
                    "date": date_text,
                    "source_url": source_url,
                    "details": details_text,
                    "responses": responses if responses else None,
                }
            )
        except Exception as e:
            logging.error(f"Error parsing complaint: {e}")

    return items