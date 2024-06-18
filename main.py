from manga_api import MangaAPI
from flask import Flask, render_template, request
import typing

app = Flask(__name__)
manga_api = MangaAPI()

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
        query = request.args.get("query").replace(" ", "_")
        data = manga_api.search_manga(query)
        results = data["data"]
        return render_template("search.html", MangaList=results)
    except (KeyError, AttributeError) as e:
        return "Invalid query or No results found (ERROR)"

@app.route("/download")
def download():
    ...
    # will work on it 

if __name__ == "__main__":
    app.run(debug=True)