try:
    import backend.global_variables as vars
except:
    import global_variables as vars

import re
import string

videoRegex = re.compile(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$")
def isVideoURL(string: str):
  return videoRegex.fullmatch(string)

playistRegex = re.compile(
    """
    ^(https|http):\/\/(?:www\.)?youtube\.com\/watch\?
    (?:&.*)*                           #extra params at the beginning
    (
        (?:
            v=([a-zA-Z0-9_\-]{11})     #propper mathing for id
            (?:&.*)*                   #extras
            &list=([a-zA-Z0-9_\-]{18}) #list
        )
        | 
        (?:
            list=([a-zA-Z0-9_\-]{18})
            (?:&.*)*                   #versa
            &v=([a-zA-Z0-9_\-]{11})
        )
    )
    (?:&.*)*                           #extras at the end
    (?:\#.*)*$     
    """
    )

# regex = re.compile("/^http:\/\/(?:www\.)?youtube\.com\/watch\?((v=[^&\s]*&list=[^&\s]*)|(list=[^&\s]*&v=[^&\s]*))(&[^&\s]*)*$/")

def isPlayistURL(string: str):
  return playistRegex.fullmatch(string)


def getVideoInfo(url):
  print("Get Video Info")


def getPlayistInfo(url):
  print("Get playist info")
