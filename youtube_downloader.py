import os
import subprocess
import platform

if __name__ == "__main__":
    print("Starting")
    path = os.path.abspath(os.path.dirname(__file__))
    ytdlp = path + ("/resources/yt-dlp_macos" if platform.system() == "Darwin" else "/resources/yt-dlp")
    subprocess.run([ytdlp, input("YouTube Link: ")])
    input()
