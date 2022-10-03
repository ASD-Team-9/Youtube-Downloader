import re
import platform
import os

isUpdating = False

singleton = None

thumbnails = []

threads = {
    "auto update thread": None,
    "downloading thread": None,
    "searching thread": None,
}

download_status = []

colours = {
    "Normal": "#33363B",
    "Normal2": "#292b2f",
    "Dark": "#202225",
    "ButtonNormal": "#36393f",
    "ButtonHover": "#5865f2",
    "ButtonHover2": "#3ba55d",
    "Text": "#b9bbbe",
}

regex = re.compile(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")

def GetPath():
    path = os.path.abspath(os.path.dirname(__file__))
    program = "yt-dlp_macos" if platform.system() == "Darwin" else "yt-dlp.exe"
    return f"{path}/../resources/{program}"
ytdlp = GetPath()

def GetFfmpeg():
    path = os.path.abspath(os.path.dirname(__file__))
    program = "ffmpeg" if platform.system() == "Darwin" else "ffmpeg.exe"
    return f"{path}/../resources/{program}"
ffmpeg = GetFfmpeg()
