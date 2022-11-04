from bbc_scraper import NewsScraper

if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.save_news(q="News", pages=1, filename='news', save_path="./news")
