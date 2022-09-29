import re

threads = {
    "auto update thread": None,
    "downloading thread": None,
    "searching thread": None,
}

colours = {
    "Normal": "#33363B",
    "Normal2": "#292b2f",
    "Dark": "#202225",
    "ButtonNormal": "#36393f",
    "ButtonHover": "#5865f2",
    "Text": "#b9bbbe",
}

regex = re.compile(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")