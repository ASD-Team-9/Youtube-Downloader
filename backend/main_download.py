import platform
import subprocess
import os
import threading

class Downloader:
    def __init__(self, frontend) -> None:
        self.frontend = frontend
        path = os.path.abspath(os.path.dirname(__file__))
        program = "yt-dlp_macos" if platform.system() == "Darwin" else "yt-dlp.exe"
        self.ytdlp = f"{path}/../resources/{program}"

        self.thread = {
            "auto update thread": None,
            "downloading thread": None,
        }
        self.auto_update()

    def do_action(self, thread_name, args):
        if (self.thread[thread_name] == None):
            self.thread[thread_name] = threading.Thread(target=self.thread_action, args=[thread_name, args])
            self.thread[thread_name].start()
            
    def thread_action(self, thread_name, args):
        subprocess.run([self.ytdlp] + args)
        self.thread[thread_name] = None

    def auto_update(self):
        self.do_action("auto update thread", ["-U"])

    def download(self, url) -> None:
        self.do_action("downloading thread", [url])
