from manga_api import MangaAPI
from flask import Flask

app = Flask(__name__)
manga_api = MangaAPI()

@app.route("/")
def main() -> dict:
    return manga_api.get_trending()

if __name__ == "__main__":
    app.run(debug=True)