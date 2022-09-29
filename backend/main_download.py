import backend.global_variables as vars
import customtkinter
import subprocess
import time
import threading

class Downloader:
    def __init__(self, frontend) -> None:
        self.frontend = frontend
        self.queue = []
        self.auto_update()

    def auto_update(self):
        def check_updating():
            vars.isUpdating = True
            subprocess.run([vars.ytdlp, "-U"])
            vars.isUpdating = False
        ActionThread("auto update thread", check_updating)

    def download(self, video_name, args) -> None:
        def begin_downloading() -> None:
            if (vars.isUpdating):
                time.sleep(0)

            while len(self.queue) > 0: #I'm under the assumption that we are using only one thread to download.
                item = self.queue.pop(0)
                try:
                    with subprocess.Popen(item.args, stdout=subprocess.PIPE, bufsize=1, shell=False, universal_newlines=True) as p:
                        for line in p.stdout:
                            data = line.split()
                            try:
                                print(data)
                                item.progress_bar.set(float(data[0].strip("%")) * 0.01)
                            except:
                                pass
                    if p.returncode != 0:
                        raise
                except:
                    print("An Error occured")

        self.queue.append(YouTubeItem(self.frontend, video_name, args))
        ActionThread("downloading thread", begin_downloading)

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
    def __init__(self, frontend, video_name, args) -> None:
        padding = 10
        width = frontend.canvas.winfo_width() - 27
        self.frame = customtkinter.CTkFrame(frontend.scrollable_frame, corner_radius=10, fg_color=vars.colours["Normal"])
        self.frame.pack(ipadx=padding, ipady=padding, pady=(0, padding))
        customtkinter.CTkLabel(self.frame, text=video_name, width=width).pack(anchor="n", pady=padding)
        self.args = [vars.ytdlp] + args
        self.progress_bar = customtkinter.CTkProgressBar(self.frame, width=width)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="top")

    def finished(self) -> None:
        pass #TODO Add a remove icon button that calls self.remove()

    def remove(self) -> None:
        self.frame.forget()