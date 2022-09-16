import os
import subprocess

if __name__ == "__main__":
    print("Starting")
    path = os.path.abspath(os.path.dirname(__file__))
    subprocess.run([path + "/resources/yt-dlp", "https://www.youtube.com/watch?v=T9eTatBQ-ic"], shell=True)
    print("Finished")
    input()