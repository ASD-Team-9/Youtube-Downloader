import global_variables as vars
import main_download

def ryan_test():
    print("Doing Ryan's Test...")
    downloader = main_download.Downloader(None)
    url = "https://www.youtube.com/watch?v=jXIy17nhPUU"
    defaultargs = ["-o", "%(title)s.%(ext)s", "--progress-template", "%(progress._percent_str)s %(progress._eta_str)s %(progress._speed_str)s"]
    downloader.download("SWR Suika's Theme: Broken Moon", [vars.ytdlp, url] + defaultargs)

def leo_test():
    print("Doing Leo's Test...")

def louis_test():
    print("Doing Louis's Test...")
    main_download.Downloader(None)

def lewis_test():
    print("Doing Lewis's Test...")

def johnny_test():
    print("Doing Johnny's Test...")

if __name__ == "__main__":
    ryan_test()
    leo_test()
    louis_test()
    lewis_test()
    johnny_test()