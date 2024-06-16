from manga_api import MangaAPI
from flask import Flask, render_template

app = Flask(__name__)
manga_api = MangaAPI()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/trending")
def trending():
    data = manga_api.get_trending()["data"][0:10]
    top_10 = [manga["title"] for manga in data]
    return render_template("trending.html", MangaList=top_10)

if __name__ == "__main__":
    app.run(debug=True)