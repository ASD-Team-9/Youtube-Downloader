import backend.global_variables as vars
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
        self.auto_update()

    def do_action(self, thread_name, args, actionDelegate = None):
        if (vars.threads[thread_name] == None):
            vars.threads[thread_name] = threading.Thread(target=self.thread_action, args=[thread_name, args, actionDelegate])
            vars.threads[thread_name].start()
            
    def thread_action(self, thread_name, args, actionDelegate):
        subprocess.run([self.ytdlp] + args)
        vars.threads[thread_name] = None
        if actionDelegate != None:
            actionDelegate()

    def auto_update(self):
        set_updating(True)
        self.do_action("auto update thread", ["-U"], lambda: set_updating(False))

    def download(self, url) -> None:
        self.do_action("downloading thread", [url])

def set_updating(bool):
    vars.isUpdating = bool