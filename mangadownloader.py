from enma import (Enma, CloudFlareConfig, ManganatoDownloader, Threaded, LocalStorage)

class MangaDownloader():
    def __init__(self) -> None:
        self.enma: Enma = Enma()
        self.enma.source_manager.set_source("manganato")
        self.downloader = ManganatoDownloader()
        self.local_storage = LocalStorage()

    def download_manga(self, Id: str, download_path, chapter) -> None:
        self.manga = self.enma.get_manga(Id)

        if self.manga:
            self.enma.download_chapter(
                path=f"{download_path}/{self.manga.title.english}",
                chapter=self.manga.chapters[chapter],
                downloader=self.downloader,
                saver=self.local_storage,
                threaded=Threaded(use_threads=True, number_of_threads=5)
            )