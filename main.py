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
        manga_data_mangadex = manga_scraper.get_mangas_mangadex(query)
        manga_data_manganato = manga_scraper.get_mangas_manganato(query)
        return render_template("select_manga.html", mangas_mangadex=manga_data_mangadex, mangas_manganato=manga_data_manganato)
    except:
        return "Invalid query or No results found (ERROR)"

def num_sort(test_string):
    return list(map(int, re.findall(r'\d+', test_string)))[0]

@app.route("/select_chapter_mangadex")
def select_chapter_mangadex():
    manga_id = request.args.get("id")
    chapter_data = manga_scraper.get_chapters_mangadex(manga_id)
    return render_template("select_chapter_mangadex.html", chapters=chapter_data)

@app.route("/select_chapter_manganato")
def select_chapter_manganato():
    manga_id = request.args.get("id")
    chapter_data = manga_scraper.get_chapters_manganato(manga_id)
    return render_template("select_chapter_manganato.html", chapters=chapter_data)

@app.route("/download")
def download():
    chapter = request.args.get("chapter")
    manga_downloader.download_chapter_imgs(chapter)
    img_list = os.listdir("static/images")
    images = []
    for img in img_list:
        images.append(os.path.join(f"images/{img}"))
        images.sort(key=num_sort)
    return render_template("download.html", images=images)

@app.route('/delete_images', methods=['POST'])
def delete_images():
    if request.json and request.json.get('action') == 'delete_images':
        for file in os.listdir("static/images"):
            os.remove(f"static/images/{file}")
        return "/"
    return "Invalid request", 400

@app.route('/manganato_test')
def manganato_test():
    query = request.args.get("query")
    manga_data = manga_scraper.get_mangas_manganato(query)
    chapter_data = manga_scraper.get_chapters_manganato(manga_data["One Piece"])
    return render_template("manganato_links.html", chapters=chapter_data)

if __name__ == "__main__":
    app.run(debug=True)