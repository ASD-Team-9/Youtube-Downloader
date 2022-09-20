import os
import subprocess
import platform

if __name__ == "__main__":
    print("Starting")
    path = os.path.abspath(os.path.dirname(__file__))

    if platform.system() == "Darwin":
        # MAC OS X
        ytdlp = path + "/resources/yt-dlp_macos"
    elif platform.system() == "Windows":
        # Windows (either 32-bit or 64-bit)
        ytdlp = path + "/resources/yt-dlp"

    subprocess.run([ytdlp,
                   "https://www.youtube.com/watch?v=T9eTatBQ-ic"])
    print("Finished Downloading")
    print("Testing to see if it works")
    input()
