import requests
from bs4 import BeautifulSoup

ENDPOINT = "https://manganato.com/search/story"
BASE_ENDPOINT = "https://chapmanganato.to/"

class Scraper():
    def __init__(self) -> None:
        pass

    def get_mangas(self, query: str):
        filtered_query: str = query.replace(" ", "_") 
        self.response = requests.get(f"{ENDPOINT}/{filtered_query}")
        self.soup = BeautifulSoup(self.response.text, "html.parser")
        self.data = self.soup.find_all("div", {"class": "search-story-item"})

        title: str = ""
        manga_id: str = ""
        manga_dict: dict = {}

        for manga in self.data:
            soup = BeautifulSoup(str(manga), "html.parser")
            title = soup.find("h3").find("a")["title"]
            manga_id = soup.find("h3").find("a")["href"].replace(BASE_ENDPOINT, "")
            manga_dict.update({title: manga_id})
        return manga_dict