import json
import os
from typing import List
from bbc_scraper.core import ScraperBBC


class NewsScraper:
    def __init__(self):
        self.scraper = ScraperBBC()

    def get_news(self, q: str, pages: int = 1) -> List[dict]:
        """
        :return: List[dict] a list of articles (dicts)
        """
        print(f"Fetching news for {q}")

        articles = self.scraper.fetch_news(q=q, pages=pages)
        self.scraper.close_session()
        if not articles:
            print(f"0 Articles were fetched for {q}")
            return []

        print(f"{len(articles)} Articles were fetched for {q}")
        return articles

    def save_news(self, q: str, pages: int = 1, filename="articles", save_path="./") -> List[dict]:
        articles = self.get_news(q=q, pages=pages)
        if not articles:
            print("Articles were not saved")
            return []
        # Make sure filename has correct extension
        if not filename.endswith(".json"):
            filename = filename + ".json"
        # Make sure directory path is closed
        if not save_path.endswith("/"):
            save_path += "/"
        # Make sure save directory exists and create it if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_path = save_path + filename
        abs_path = os.path.abspath(file_path)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(articles, f, indent=2)
                print(f"Articles were successfully saved to {abs_path}")
        except Exception as e:
            print(e)
            print("Failed to save articles")
            return []

        return articles
