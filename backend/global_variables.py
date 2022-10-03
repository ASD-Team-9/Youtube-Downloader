import re
import platform
import os

#The singleton frontend
globalFrontend = None

#A list to hold all the references of thumbnail images as Python cleans images aggressively.
thumbnails = []

#Responsible for holding all the threads.
threads = {
    "auto update thread": None,
    "downloading thread": None,
    "searching thread": None,
}

#Dictionary of the project's colour palette.
colours = {
    "Normal": "#33363B",
    "Normal2": "#292b2f",
    "Dark": "#202225",
    "ButtonNormal": "#36393f",
    "ButtonHover": "#5865f2",
    "ButtonHover2": "#3ba55d",
    "Text": "#b9bbbe",
}

#Used for checking if a YouTube URL is valid or not.
regex = re.compile(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")

#Not to be used anywhere but here but grabs the path of the downloader.
def _GetPath():
    path = os.path.abspath(os.path.dirname(__file__))
    program = "yt-dlp_macos" if platform.system() == "Darwin" else "yt-dlp.exe"
    return f"{path}/../resources/{program}"
ytdlp = _GetPath()