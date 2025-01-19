import requests
from bs4 import BeautifulSoup
from .eol_scraper import EOLScraper

class WebCrawler:
    def __init__(self):
        self.scraper = EOLScraper()

    def google_search(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        return response.text

    def parse_results(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for g in soup.find_all('div', class_='BVG0Nb'):
            link = g.find('a')['href']
            results.append(link)
        return results

    def crawl(self, product_name):
        query = f"{product_name} end of life"
        html = self.google_search(query)
        urls = self.parse_results(html)
        eol_data = self.scraper.crawl_and_scrape(urls)
        return eol_data