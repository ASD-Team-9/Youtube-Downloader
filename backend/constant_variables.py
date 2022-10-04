"The constant variables for the program."
import re
import platform
import os
from pathlib import Path
from backend.main_download import Downloader
from backend.action_thread import ActionThread

#The singleton frontend and downloader
FRONTEND = None
DOWNLOADER: Downloader = None
AZURE_TEST = False

#A list to hold all the references of thumbnail images as Python cleans images aggressively.
THUMBNAILS = []

#Responsible for holding all the threads.
THREADS: dict[str, ActionThread] = {
    "auto update thread": None,
    "downloading thread": None,
    "searching thread": None,
}

#Dictionary of the project's colour palette.
THEME = "Default"
COLOURS: dict[str, dict[str, (str, str)]] = {
    "Mode": { #DO NOT USE BUT FOLLOW.
        "Example": ("#LightMode", "#DarkMode"),
    },

    "Default": {
        "Normal": "#33363B",
        "Normal2": "#292b2f",
        "Dark": "#202225",
        "ButtonNormal": "#36393f",
        "ButtonHover": "#5865f2",
        "ButtonHover2": "#3ba55d",
        "Text": "#b9bbbe",
    },
}
def get_colour(palette_name: str):
    "Simplifies the process of getting the colour."
    return COLOURS[THEME][palette_name]

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
