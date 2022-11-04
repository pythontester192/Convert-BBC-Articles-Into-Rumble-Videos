from typing import List
from bbc_scraper.core import Client
from bbc_scraper.core import GoogleScraper
from bbc_scraper.core import NewsFormatter


class ScraperBBC(Client):
    def __init__(self):
        HEADERS = {
            "DNT": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "Keep-Alive"}
        super().__init__(headers=HEADERS)
        self._news_source = "www.bbc.com"
        self._google = GoogleScraper(website=self._news_source)
        self._formatter = NewsFormatter()

    def fetch_news(self, q: str, pages: int = 1) -> List[dict]:
        links = self._google.search(q=q, pages=pages)
        if not links:
            print(f"No results found for {q} on www.google.com.")
            return []

        pages_html = self._fetch_pages_html(links)
        if not pages_html:
            print(f"Failed to fetch pages from {self._news_source}")
            return []

        try:
            articles = self._formatter.format_articles(pages_html)
            return articles
        except Exception as e:
            print(f"Failed to format articles, {e}")
            return []

    def _fetch_pages_html(self, links) -> List[str]:
        return [x for x in self.__fetch_pages_html(links)]

    def __fetch_pages_html(self, links) -> str:
        for link in links:
            if "www.bbc.com/news/" not in link:
                continue
            response = self.request(link)
            if response is None:
                continue
            yield response.text
