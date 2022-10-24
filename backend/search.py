"The youtube search backend."
import backend.constant_variables as CONST

def is_video_url(string: str) -> bool:
    "Checks if given string is a video URL"
    return CONST.VIDEO_REGEX.fullmatch(string)

def is_playist_url(string: str) -> bool:
    "Checks if given string is a YouTube playlist"
    return "list" in string and is_video_url(string)
