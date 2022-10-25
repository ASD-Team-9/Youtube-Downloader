"This is a test file for Azure Pipeline automated testing."
import threading
from time import sleep
from unittest import TestCase
import backend.constant_variables as CONST

def pipeline_test():
    "The main pipeline test"
    def johnny_test():
        print("Doing Johnny's Test...")
        video_id = "_oRxHF8GiUE"
        title = "Lullaby 「Frozen Starfall」"
        CONST.DOWNLOADER.download({"id": video_id, "title": title}, "Best Video", "Highest")
        CONST.DOWNLOADER.download({"id": video_id, "title": title}, "Best Audio", "Highest")
        CONST.DOWNLOADER.download({"id": video_id, "title": title}, "mp4", "Highest")
        CONST.DOWNLOADER.download({"id": video_id, "title": title}, "mp4", "Normal")
        CONST.DOWNLOADER.download({"id": video_id, "title": title}, "mp4", "Lowest")
        CONST.DOWNLOADER.download({"id": video_id, "title": title}, "mp3", "Highest")

    def leo_test():
        print("Doing Leo's Test...")

    def lewis_test():
        print("Doing Lewis's Test")

    def louis_test():
        print("Doing Louis's Test - Auto update feature")
        CONST.DOWNLOADER.update_downloader()

    def ryan_test():
        print("Doing Ryan's Test...")

        print("Downloading a video...")
        video_id = "_oRxHF8GiUE"
        title = "Lullaby 「Frozen Starfall」"
        CONST.DOWNLOADER.download({"id": video_id, "title": title}, "Best Audio", "Highest")

    while CONST.FRONTEND is None:
        sleep(1)

    for each_test in [johnny_test, leo_test, lewis_test, louis_test, ryan_test]:
        status = "Failed"
        try:
            each_test()
            status = "Success"
        except Exception as exception:
            print(exception)
        finally:
            print(f"{status}: {each_test.__name__}\n")

    waiting = True
    while waiting:
        waiting = False
        for thread in CONST.THREADS.items():
            waiting = waiting or thread[1] is not None
            if waiting:
                break

    CONST.FRONTEND.quit()
    print("Testing finished!")

def start_test():
    "Begin the azure test"
    threading.Thread(target=pipeline_test).start()

if __name__ == "__main__":
    CONST.AZURE_TEST = True
    from frontend.frontend import FrontEnd
    FrontEnd()
