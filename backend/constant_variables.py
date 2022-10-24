"The constant variables for the program."
import re
import platform
import os
from pathlib import Path

#The singleton frontend and downloader
FRONTEND = None
DOWNLOADER = None

#Boolean check to output certain functions onto the console.
AZURE_TEST = False

#A list to hold all the references of thumbnail images as Python cleans images aggressively.
THUMBNAILS = []

#Responsible for holding all the threads.
THREADS: dict[str] = {
    "auto update thread": None,
    "downloading thread": None,
    "searching thread": None,
    "browsing thread": None,
    "playlist loading thread": None,

    "video loading thread": None,
    "video looping thread": None,
    "volume update thread": None,
}

#Used for checking if a YouTube URL is valid or not.
VIDEO_REGEX = re.compile(
    r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))" +
    r"(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
)

#TODO: Grab the preference from file.
DOWNLOAD_PATH = str(Path.home() / "Downloads")

def _ytdlp():
    "Should only be called once. Grabs the path of the ytdlp program"
    path = os.path.abspath(os.path.dirname(__file__))
    program = "yt-dlp_macos" if platform.system() == "Darwin" else "yt-dlp.exe"
    return f"{path}/../resources/{program}"
YTDLP = _ytdlp()

def _ffmpeg():
    "Should only be called once. Grabs the path of the ffmpeg program"
    path = os.path.abspath(os.path.dirname(__file__))
    program = "ffmpeg" if platform.system() == "Darwin" else "ffmpeg.exe"
    return f"{path}/../resources/{program}"
FFMPEG = _ffmpeg()
