import requests
import os 
from dotenv import load_dotenv

ENDPOINT = "https://mangareader-api.vercel.app/api/v1"

class MangaAPI:
    def __init__(self) -> None:
        load_dotenv()

    def get_featured(self) -> dict:
        response = requests.get(f"{ENDPOINT}/featured")
        return response.json()

    def get_trending(self) -> dict:
        response = requests.get(f"{ENDPOINT}/trending")
        return response.json()

    def get_manga(self, slug: str) -> dict:
        params: dict = {
            "slug": slug,
        }
        response = requests.get(f"{ENDPOINT}/manga", params=params)
        return response.json()

    def search_manga(self, query: str) -> dict:
        params: dict = {
            "query": query,
        }
        response = requests.get(f"{ENDPOINT}/search", params=params)
        return response.json()