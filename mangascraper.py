import requests
from bs4 import BeautifulSoup

ENDPOINT = "https://manganato.com/search/story"

class Scraper():
    def __init__(self) -> None:
        pass

    def get_mangas(self, query: str):
        filtered_query: str = query.replace(" ", "_") 
        self.response = requests.get(f"{ENDPOINT}/{filtered_query}")
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.manga_list: list = []
        return self.soup.find_all("div", {"class": "search-story-item"})
scraper = Scraper()
print(scraper.get_mangas("one piece"))