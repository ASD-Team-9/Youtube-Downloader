"A class to help update the frontend queue."
import customtkinter
import backend.constant_variables as CONST

class DownloadItem():
    "A simple class to update the frontend queue."
    def __init__(self, video_name, args) -> None:
        padding = 10
        width = CONST.FRONTEND.canvas.winfo_width() - 27

        self.frame = customtkinter.CTkFrame(
            CONST.FRONTEND.scrollable_frame, corner_radius=10, fg_color=CONST.get_colour("Normal")
        )
        self.frame.pack(ipadx=padding, ipady=padding, pady=(0, padding))

        customtkinter.CTkLabel(
            self.frame, text=video_name, width=width
        ).pack(anchor="n", pady=padding)
        self.args = args
        self.progress_bar = customtkinter.CTkProgressBar(self.frame, width=width)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="top")

    def finished(self, success) -> None:
        "A method called after the download whether it was successful or not."
        #TODO Add a remove icon button that calls self.remove()

    def remove(self) -> None:
        "Removes the widget from the queued list in the "
        self.frame.forget()