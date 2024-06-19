import requests
import img2pdf
import os

# MANGANATO_ENDPOINT = "https://chapmanganato.to"
MANGADEX_ENDPOINT = "https://api.mangadex.org/at-home/server"
class MangaDownloader:
    def __init__(self) -> None:
        pass

    # Gets urls from https://api.mangadex.org/docs/ (api reference)
    def get_download_urls(self, id: str) -> list:
        response = requests.get(f"{MANGADEX_ENDPOINT}/{id}")
        data: dict = response.json()
        base_url: str = data["baseUrl"]
        url_hash: str = data["chapter"]["hash"]
        download_url_list = []

        for self.chapter in data["chapter"]["data"]:
            download_url: str = f"{base_url}/data/{url_hash}/{self.chapter}"
            download_url_list.append(download_url)
        return download_url_list


### Code below only works for local apps not HTML ###
    def download_chapter_imgs(self, id: str, path: str) -> None:
        self.count: int = 0

        # Get the urls from the mangadex server (returns json)
        response = requests.get(f"{MANGADEX_ENDPOINT}/{id}")
        data: dict = response.json()

        # Filter the json to get the relevant info
        base_url: str = data["baseUrl"]
        url_hash: str = data["chapter"]["hash"]

        for self.chapter in data["chapter"]["data"]:
            download_url: str = f"{base_url}/data/{url_hash}/{self.chapter}"

            # Starts a download session and downloads the image
            self.session = requests.Session()
            response = self.session.get(download_url, stream=True)

            self.count += 1
            os.makedirs(f"{path}/imgsrc", exist_ok=True)

            with open(f"{path}/imgsrc/{self.count}.jpg", "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        self.download_chapter_pdf(path)

# Converts file to PDF
    def download_chapter_pdf(self, path: str) -> None:
        # Opening the image file
        with open(f"{path}/imgsrc/{self.count}.jpg", "rb") as f:
            img_files = [open(f"{path}/imgsrc/{i}", "rb").read() for i in os.listdir("imgsrc") if i.endswith(".jpg")]
            pdf_data = img2pdf.convert(img_files)

        # Creating a pdf file and removing the imgs
            with open(f"{path}/{self.chapter}.pdf", "wb") as pdf_file:
                pdf_file.write(pdf_data)
            for file in os.listdir(f"{path}/imgsrc"):
                os.remove(f"{path}/imgsrc/{file}")
### Code above only works for local apps not HTML ###


### TEMPORARILY DISABLED MANGANATO DUE TO CLOUDFLARE BLOCK ###

#         self.session = requests.Session()
#         self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#         self.cookies: dict = {
#             "content_server": "server2"
#         }

#     def query_download_links(self, id: str) -> None:
#         response = self.session.get(f"{ENDPOINT}/{id}", cookies=self.cookies, impersonate="chrome110")
#         soup = BeautifulSoup(response.text, "html.parser")

#         chapter_links = [f"{chapter.find('a')['href']}" for chapter in soup.find_all("li", {"class": "a-h"})]
#         chapters = [chapter.find('a')['href'].replace(f"{ENDPOINT}/{id}/", "") for chapter in soup.find_all("li", {"class": "a-h"})]

#         # with ThreadPoolExecutor(max_workers=20) as executor:
#         #     executor.map(self.download_chapter, (chapter_links[0], chapters[0]))

#         print(chapter_links[10])
#         self.download_chapter(chapter_links[10], chapters[10])

#     def download_chapters(self, link, manga_chapter):
#         chapter_link = link
#         chapter = manga_chapter
#         response = self.session.get(chapter_link, cookies=self.cookies, impersonate="chrome110")
#         soup = BeautifulSoup(response.text, "html.parser")

#         for img in soup.find_all("img"):
#             time.sleep(3)
#             src = img.get("src")
#             print(src)
#             response = self.session.get(src, stream=True, cookies=self.cookies, impersonate="chrome110")
#             print(response)
#             print(self.session.headers)
#             with open(f"{chapter}.jpg", "wb") as f:
#                 for chunk in response.iter_content(chunk_size=1024):
#                     if chunk:
#                         f.write(chunk)