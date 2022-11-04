from typing import List
from bs4 import BeautifulSoup
from bs4.element import Tag as Element
from bbc_scraper.core import Client


class GoogleScraper(Client):
    def __init__(self, website=None):
        HEADERS = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Alt-Used": "www.google.com",
            "Connection": "Keep-Alive",
            "DNT": "1",
            "TE": "trailers"}
        super().__init__(headers=HEADERS)
        self._result_class = "yuRUbf"
        self.website = website

    def search(self, q: str, pages: int = 1) -> List[str]:
        KEYWORD = q.replace(" ", "+")
        if self.website:
            URL = f'https://www.google.com/search?q="{KEYWORD}"+site:{self.website}'
        else:
            URL = f'https://www.google.com/search?q="{KEYWORD}"'

        links = self._fetch_links(URL, pages)

        # End session to save resources
        self.close_session()

        return links

    def _fetch_links(self, url: str, pages: int) -> List[str]:
        if pages > 1:
            links = self._fetch_pages_links(url, pages=pages)
        else:
            response = self.request(url)
            if response is None:
                return []
            soup = BeautifulSoup(response.text, "html.parser")
            result_links = soup.find_all("div", {"class": "yuRUbf"})
            links = self._fetch_page_links(result_links)
        return links

    def _fetch_pages_links(self, url, pages: int) -> List[str]:
        pages_url = url + "&start="
        links = list()
        for i in range(1, pages + 1):
            temp_url = pages_url + str(i * 10)
            response = self.request(temp_url)
            if response is None:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            result_links = soup.find_all("div", {"class": self._result_class})
            if not result_links:
                break
            links += self._fetch_page_links(result_links)

        return links

    @staticmethod
    def _fetch_page_links(results: List[Element]) -> List[str]:
        links = list()
        for x in results:
            try:
                link = x.find("a").get("href")
                links.append(link)
            except:
                continue
        return links
