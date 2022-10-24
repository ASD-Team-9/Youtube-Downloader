"This is the main downloading class"
import subprocess
import time

from frontend.download_item import DownloadItem
from backend.action_thread import ActionThread
import backend.constant_variables as CONST
import backend.format as Format

class Downloader:
    """
    This is the main downloader class.

    Methods:
        update_downloader()\n
        download(video_name, args)\n
        download_audio(url)\n
    """
    def __init__(self) -> None:
        self.queue = []

        with open("resources/update.txt", "r", encoding="utf-8") as file:
            if file.readline() == "enabled":
                self.update_downloader()

    def get_default_args(self) -> list[str]:
        "Getting the default arguements"
        return [
            "-o", f"{CONST.DOWNLOAD_PATH}/%(title)s.%(ext)s",
            "--progress-template",
            "%(progress._percent_str)s %(progress._eta_str)s %(progress._speed_str)s"
        ]

    def update_downloader(self) -> None:
        "Updates the downloader. Simply calling this is enough."
        def check_updating():
            subprocess.run([CONST.YTDLP, "-U"], check=True)
        ActionThread("auto update thread", check_updating)

    def download(self, video_details: dict, format_type: str, quality_type: str) -> None:
        """
        Download a video by using threads

        Parameters: video_details, format_type, quality_type

        video_details: The video details in dictionary
        format_type: Type of format in string
        quality_type: Type of quality in string
        """
        def begin_downloading() -> None:
            if CONST.THREADS["auto update thread"] is not None:
                time.sleep(0)

            #I'm under the assumption that we are using only one thread to download.
            while len(self.queue) > 0:
                item = self.queue.pop(0)
                if CONST.AZURE_TEST:
                    subprocess.run(item.args, check=True)
                    continue

                with subprocess.Popen(
                    item.args, stdout=subprocess.PIPE,
                    bufsize=1, shell=False, universal_newlines=True
                ) as process:
                    for line in process.stdout:
                        data = line.split()
                        try:
                            item.progress_bar.set(float(data[0].strip("%")) * 0.01)
                        except Exception:
                            pass
                if process.returncode != 0:
                    print("ERROR HERE") #TODO: Update failure on queued item
        download_url = (
            [CONST.YTDLP, "https://www.youtube.com/watch?v=" + video_details["id"]] +
            self.get_default_args() +
            Format.update_video_args(format_type, quality_type)
        )
        self.queue.append(DownloadItem(video_details["title"], download_url))
        ActionThread("downloading thread", begin_downloading)

    def download_audio(self, url):
        "Auto converts a video into audio??"
        # ffmpeg -i input.m4a -vn -ar 44100 -ac 2 -b:a 192k output.mp3
        # ffmpeg -i audio.wav -acodec libmp3lame audio.mp3
        print("Starting downloading audio")
        print(url)
