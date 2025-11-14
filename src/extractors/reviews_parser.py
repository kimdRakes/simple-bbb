thonpython
import logging
from bs4 import BeautifulSoup
from typing import List, Dict

def parse_reviews(soup: BeautifulSoup, base_url: str) -> List[Dict]:
    items = []

    reviews = soup.select(".review, .Review, .customer-review")
    if not reviews:
        logging.warning("No reviews found on page.")

    for r in reviews:
        try:
            category = "Review"
            user = r.select_one(".consumer-name, .reviewer, .user").get_text(strip=True) if r.select_one(
                ".consumer-name, .reviewer, .user"
            ) else None
            stars = None
            star_el = r.select_one(".star-rating, .rating")
            if star_el and star_el.get("data-rating"):
                stars = int(star_el.get("data-rating"))

            date = r.select_one(".date-posted, .date, time")
            date_text = date.get_text(strip=True) if date else None

            details = r.select_one(".description, .content, .review-text")
            details_text = details.get_text(strip=True) if details else None

            source = r.select_one("a")
            source_url = source["href"] if source and source.has_attr("href") else base_url

            items.append(
                {
                    "category": category,
                    "user": user,
                    "status": None,
                    "type": None,
                    "stars": stars,
                    "date": date_text,
                    "source_url": source_url,
                    "details": details_text,
                    "responses": None,
                }
            )
        except Exception as e:
            logging.error(f"Error parsing review: {e}")

    return items