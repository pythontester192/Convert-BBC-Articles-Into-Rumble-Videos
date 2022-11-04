import requests
from bbc_scraper.utils import user_agent


class Client:
    def __init__(self, headers: dict):
        self._headers = headers
        self._session = None

    def request(self, url: str) -> requests.Response | None:
        if self._session is None:
            self.start_session()
        try:
            response = self._session.get(url)
        except:
            print(f"Couldn't connect to {url}")
            return None

        if response.status_code != 200:
            print(f"Bad response from {url}")
            return None

        return response

    def start_session(self):
        self._headers["User-Agent"] = user_agent()
        self._session = requests.session()
        self._session.headers.update(self._headers)

    def close_session(self):
        if self._session is not None:
            self._session.close()
            self._session = None
