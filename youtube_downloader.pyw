import frontend.frontend

#Required modules:
    #pip install customtkinter==0.3
    #pip install youtube-search-python

if __name__ == "__main__":
    #path = os.path.abspath(os.path.dirname(__file__))
    #ytdlp = path + ("/resources/yt-dlp_macos" if platform.system() == "Darwin" else "/resources/yt-dlp")
    #subprocess.run([ytdlp, input("YouTube Link: ")])
    frontend.frontend.FrontEnd()
