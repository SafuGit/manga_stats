from manga_api import MangaAPI
from mangascraper import Scraper
from mangadownloader import MangaDownloader
from flask import Flask, render_template, request
import re
import os

app = Flask(__name__)
manga_api = MangaAPI()
manga_scraper = Scraper()
manga_downloader = MangaDownloader()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/trending")
def trending():
    data = manga_api.get_trending()["data"][0:10]
    top_10 = [{"rank": index + 1, "title": manga["title"]} for index, manga in enumerate(data)]
    return render_template("trending.html", MangaList=top_10)

@app.route("/featured")
def featured():
    data = manga_api.get_featured()["data"][0:10]
    top_10 = [{"rank": index + 1, "title": manga["title"]} for index, manga in enumerate(data)]
    return render_template("featured.html", MangaList=top_10)

@app.route("/search")
def search():
    try:
        query = request.args.get("query")
        manga_data = manga_scraper.get_mangas_mangadex(query)
        return render_template("select_manga.html", mangas=manga_data)
    except:
        return "Invalid query or No results found (ERROR)"

def num_sort(test_string):
    return list(map(int, re.findall(r'\d+', test_string)))[0]

@app.route("/select_chapter")
def select_chapter():
    manga_id = request.args.get("id")
    chapter_data = manga_scraper.get_chapters_mangadex(manga_id)
    return render_template("select_chapter.html", chapters=chapter_data)

@app.route("/download")
def download():
    chapter = request.args.get("chapter")
    return chapter
    # manga_downloader.download_chapter_imgs(chapter_data["1"])
    # img_list = os.listdir("static/images")
    # images = []
    # for img in img_list:
    #     images.append(os.path.join(f"images/{img}"))
    #     images.sort(key=num_sort)
    # return render_template("download.html", images=images)
if __name__ == "__main__":
    app.run(debug=True)