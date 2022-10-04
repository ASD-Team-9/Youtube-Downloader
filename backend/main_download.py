try:
    import backend.global_variables as vars
except:
    import global_variables as vars

import customtkinter
import subprocess
import time
import threading

class Downloader:
    def __init__(self) -> None:
        self.queue = []
        self.auto_update() #TODO: Read from preferences and choose to auto update or not.

    def auto_update(self):
        def check_updating():
            subprocess.run([vars.ytdlp, "-U"])
        ActionThread("auto update thread", check_updating)

    """
    Download a video by using threads

    Parameters:

    video_name: The video title
    args: The arguements/options from yt-dlp
    """
    def download(self, video_name, args) -> None:
        def begin_downloading() -> None:
            if (vars.threads["auto update thread"] != None):
                time.sleep(0)

            while len(self.queue) > 0: #I'm under the assumption that we are using only one thread to download.
                item = self.queue.pop(0)
                try:
                    with subprocess.Popen(item.args, stdout=subprocess.PIPE, bufsize=1, shell=False, universal_newlines=True) as p:
                        for line in p.stdout:
                            data = line.split()
                            try:
                                item.progress_bar.set(float(data[0].strip("%")) * 0.01)
                            except:
                                pass
                    if p.returncode != 0:
                        raise
                except Exception as e:
                    print(item.args)
                    print("An Error occured")

        self.queue.append(YouTubeItem(video_name, args))
        ActionThread("downloading thread", begin_downloading)

    def downloadAudio(self, url):
        # ffmpeg -i input.m4a -vn -ar 44100 -ac 2 -b:a 192k output.mp3
        # ffmpeg -i audio.wav -acodec libmp3lame audio.mp3
        print("Starting downloading audio")
        print(url)

class ActionThread:
    def __init__(self, thread_name, actionDelegate) -> None:
        def thread_action():
            self.actionDelegate()
            vars.threads[self.name] = None

        if (vars.threads[thread_name] == None):
            self.name = thread_name
            self.actionDelegate = actionDelegate
            vars.threads[thread_name] = threading.Thread(target=thread_action)
            vars.threads[thread_name].start()

class YouTubeItem():
    def __init__(self, video_name, args) -> None:
        padding = 10
        width = vars.globalFrontend.canvas.winfo_width() - 27
        self.frame = customtkinter.CTkFrame(vars.globalFrontend.scrollable_frame, corner_radius=10, fg_color=vars.colours["Normal"])
        self.frame.pack(ipadx=padding, ipady=padding, pady=(0, padding))
        customtkinter.CTkLabel(self.frame, text=video_name, width=width).pack(anchor="n", pady=padding)
        self.args = args
        self.progress_bar = customtkinter.CTkProgressBar(self.frame, width=width)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="top")

    def finished(self, success) -> None:
        pass #TODO Add a remove icon button that calls self.remove()

    def remove(self) -> None:
        self.frame.forget()
