import requests
import json

MANGADEX_ENDPOINT = "https://api.mangadex.org"

class Scraper():
    def __init__(self) -> None:
        pass

    def get_mangas_mangadex(self, query: str) -> dict:
        response = requests.get(f"{MANGADEX_ENDPOINT}/manga", params={"title": query,})
        return {manga["attributes"]["title"]["en"]: manga["id"] for manga in response.json()["data"]}

    def get_chapters_mangadex(self, manga_id: str) -> dict:
        response = requests.get(f"{MANGADEX_ENDPOINT}/manga/{manga_id}/feed", params={"translatedLanguage[]": "en", "limit": 500})
        data = response.json()

        chapters = {item['attributes']["chapter"]: item["id"] for item in data["data"]}
        return chapters

### TEMPORARILY DISABLED MANGANATO DUE TO CLOUDFLARE BLOCK ###

    # def get_mangas_manganato(self, query: str):
    #     filtered_query: str = query.replace(" ", "_") 
    #     self.response = requests.get(f"{ENDPOINT}/{filtered_query}")
    #     self.soup = BeautifulSoup(self.response.text, "html.parser")
    #     self.data = self.soup.find_all("div", {"class": "search-story-item"})

    #     title: str = ""
    #     manga_id: str = ""
    #     manga_dict: dict = {}

    #     for manga in self.data:
    #         soup = BeautifulSoup(str(manga), "html.parser")
    #         title = soup.find("h3").find("a")["title"]
    #         manga_id = soup.find("h3").find("a")["href"]
    #         manga_dict.update({title: manga_id})
    #     return manga_dict