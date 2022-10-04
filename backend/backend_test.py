import global_variables as vars
import main_download
import subprocess

def ryan_test():
    print("Doing Ryan's Test...")
    
    print("Downloading a video...")
    url = "https://www.youtube.com/watch?v=jXIy17nhPUU"
    defaultargs = ["-o", "%(title)s.%(ext)s", "--progress-template", "%(progress._percent_str)s %(progress._eta_str)s %(progress._speed_str)s"]
    subprocess.Popen([vars.ytdlp, url] + defaultargs)

def leo_test():
    print("Doing Leo's Test...")

def louis_test():
    print("Doing Louis's Test...")
    main_download.Downloader()

def lewis_test():
    print("Doing Lewis's Test")

def johnny_test():
    print("Doing Johnny's Test...")
    url = "https://www.youtube.com/watch?v=qIQ3xNqkVC4"

    try: 
        main_download.Downloader.downloadAudio(None, url)
        print("Successfully pass Johnny test")
    except:
        print("Failed to pass Johnny test")

if __name__ == "__main__":
    ryan_test()
    leo_test()
    louis_test()
    lewis_test()
    johnny_test()
    print("Successfully pass all tests")
