"This is a test file for Azure Pipeline automated testing."
import threading
from time import sleep
import backend.constant_variables as CONST
from frontend.frontend import FrontEnd

def pipeline_test():
    "The main pipeline test"
    def johnny_test():
        print("Doing Johnny's Test...")
        url = "https://www.youtube.com/watch?v=qIQ3xNqkVC4"

    def leo_test():
        print("Doing Leo's Test...")

    def lewis_test():
        print("Doing Lewis's Test")

    def louis_test():
        print("Doing Louis's Test...")

    def ryan_test():
        print("Doing Ryan's Test...")

        print("Downloading a video...")
        url = "https://www.youtube.com/watch?v=_oRxHF8GiUE"
        CONST.FRONTEND.download("Lullaby 「Frozen Starfall」", [CONST.YTDLP, url])

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

if __name__ == "__main__":
    CONST.AZURE_TEST = True
    threading.Thread(target=pipeline_test).start()
    FrontEnd()
