import platform
import subprocess
import os
import threading

class Downloader:
    def __init__(self, frontend) -> None:
        self.frontend = frontend
        path = os.path.abspath(os.path.dirname(__file__))
        program = "yt-dlp_macos" if platform.system() == "Darwin" else "yt-dlp.exe"
        self.ytdlp = f"{path}/../resources/{program}"

        self.thread = None

    def download(self, url) -> None:
        self.thread = threading.Thread(target=self.thread_download, args=[url])
        self.thread.start()

    def thread_download(self, url) -> None:
        subprocess.run([self.ytdlp, url])
