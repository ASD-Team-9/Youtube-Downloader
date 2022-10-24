"The main frontend class"
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import customtkinter
import youtubesearchpython as YouTube

import frontend.color as COLOR
import frontend.pages as Pages
import backend.constant_variables as CONST
import backend.search as searcher
from backend.action_thread import ActionThread
from backend.main_download import Downloader

class FrontEnd(customtkinter.CTk):
    "The main class for the front end."
    def __init__(self) -> None:
        if CONST.FRONTEND is None:
            super().__init__()
            self.current_page = None
            CONST.FRONTEND = self
            CONST.DOWNLOADER = Downloader()
            self._set_main_settings()
            self._set_left_frame()
            self._set_right_frame()
            self.mainloop()

    def _set_main_settings(self) -> None:
        "Setting the main settings."
        self.width = 1280
        self.height = 720
        self.geometry(f"{self.width}x{self.height}")
        self.title("YouTube Downloader")
        self.configure(bg=COLOR.get_colour("Normal"))
        self.resizable(False, False)

    def _set_left_frame(self) -> None:
        "Creates the left frame for the structure of the frontend."
        third = self.width / 3
        padding = 10
        left_frame_width = third - padding * 2

        left_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR.get_colour("Dark"), corner_radius=0
        )
        left_frame.pack(
            side=tkinter.LEFT, anchor="nw", fill=tkinter.Y,
            ipadx=padding, ipady=padding
        )

        def set_left_top_frame(self: FrontEnd) -> None:
            def auto_search(self: FrontEnd): #The event parameter is needed.
                if CONST.THREADS["searching thread"] is None:
                    clipboard = self.clipboard_get()
                    if clipboard != self.entry.get() and searcher.is_video_url(clipboard):
                        self.clear_entry()
                        self.entry.insert(0, clipboard)
                        search_entry(self)

            def search_entry(self: FrontEnd) -> None:
                search = self.entry.get()
                if search != "":
                    ActionThread("searching thread", lambda: self.thread_search(search))

            left_top_frame = customtkinter.CTkFrame(
                left_frame, fg_color=COLOR.get_colour("Normal2"), height=self.height * 0.1
            )
            left_top_frame.pack(
                side=tkinter.TOP, anchor="nw", fill=tkinter.X,
                padx=padding, pady=padding, ipady=padding
            )

            self.entry = customtkinter.CTkEntry(
                left_top_frame, width=left_frame_width - 134, height=40, placeholder_text="Search"
            )
            self.entry.pack(side="left", padx=(padding, 0))
            self.entry.bind("<Enter>", lambda e: auto_search(self))
            self.entry.bind("<Return>", lambda e: search_entry(self))

            clear_icon = get_image("ClearIcon.png").subsample(4)
            search_icon = get_image("SearchIcon.png").subsample(3)
            width = ((clear_icon.width() + search_icon.width()) * 0.5) + padding
            height = ((clear_icon.height() + search_icon.height()) * 0.5) + padding
            customtkinter.CTkButton(
                left_top_frame, image=clear_icon, width=width, height=height,
                fg_color=COLOR.get_colour("ButtonNormal"),
                hover_color=COLOR.get_colour("ButtonHover"),
                text="", command=self.clear_entry
            ).pack(side="left", fill=tkinter.X, expand=True, padx=(padding, 0))

            customtkinter.CTkButton(
                left_top_frame, image=search_icon, width=width, height=height,
                fg_color=COLOR.get_colour("ButtonNormal"),
                hover_color=COLOR.get_colour("ButtonHover"),
                text="", command=lambda: search_entry(self)
            ).pack(side="left", fill=tkinter.X, expand=True, padx=padding)
        set_left_top_frame(self)

        def set_left_middle_frame(self: FrontEnd) -> None:
            left_middle_frame = customtkinter.CTkFrame(
                left_frame, fg_color=COLOR.get_colour("Normal2")
            )
            left_middle_frame.pack(side="top", fill=tkinter.BOTH, expand=True, padx=padding)

            self.canvas = tkinter.Canvas(
                left_middle_frame, highlightthickness=0,
                width=left_frame_width - padding * 5
            )

            scrollbar = customtkinter.CTkScrollbar(
                left_middle_frame,
                fg_color=COLOR.get_colour("Normal2"),
                command=self.canvas.yview
            )
            scrollbar.pack(side="right", fill="y", padx=(0, 3))

            self.scrollable_frame = tkinter.Frame(self.canvas, bg=COLOR.get_colour("Normal2"))
            self.scrollable_frame.bind(
                "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )
            self.scrollable_frame.pack(fill="both", expand=True)

            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=scrollbar.set, bg=COLOR.get_colour("Normal2"))
            self.canvas.bind_all(
                "<MouseWheel>",
                lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            )
            self.canvas.pack(side="left", fill="both", expand=True, padx=(padding, 0), pady=padding)
        set_left_middle_frame(self)

        def set_left_bottom_frame(self: FrontEnd) -> None:
            left_bottom_frame = customtkinter.CTkFrame(
                left_frame, fg_color=COLOR.get_colour("Normal2"), height=self.height * 0.1
            )
            left_bottom_frame.pack(anchor="n", fill=tkinter.X, padx=10, pady=10)

            def image_buttons(image_name: str, subsample: int, command) -> None:
                logo = get_image(image_name).subsample(subsample)
                customtkinter.CTkButton(
                    left_bottom_frame, image=logo,
                    width=logo.width() + 10, height=logo.height() + 10,
                    fg_color=COLOR.get_colour("ButtonNormal"),
                    hover_color=COLOR.get_colour("ButtonHover"),
                    text="", command=command
                ).pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=10, pady=10)
            image_buttons("SettingsIcon.png", 3, lambda: self.change_page("Settings Page"))
            image_buttons("Logo.png", 83, lambda: self.change_page("Account Page"))
        set_left_bottom_frame(self)

    def _set_right_frame(self) -> None:
        "Creates the right frame for the structure of the frontend. Should only be called once."
        self.right_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR.get_colour("Normal"), corner_radius=0
        )

        #Fill
        customtkinter.CTkFrame(
            self.right_frame, height=0, width = self.width * 2 / 3, corner_radius=0
        ).pack(anchor="nw")

        self.pages = {
            #"Page Name" : Pages.methodOfPage()
            "Settings Page" : Pages.settings_page(),
            "Account Page" : Pages.account_page(),
            "New Account Page" : Pages.new_account_page(),
            "History Page" : Pages.history_page(),
            "Video Player" : Pages.video_player(),
            "Unknown Page" : customtkinter.CTkFrame(
                corner_radius=0, fg_color=COLOR.get_colour("Normal")
            )
            
        }
        self.current_page = None

        self.right_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    def change_page(self, page: str) -> None:
        "Updates and changes the right frame of the frontend."
        if self.current_page is not None:
            self.current_page.forget()
        self.current_page = self.pages[page]
        self.current_page.pack(fill="both", expand=True)

    def clear_entry(self, auto_refocus: bool = True) -> None:
        "Clears the entry of the search bar"
        self.entry.delete(0, tkinter.END)
        self.focus()
        CONST.THUMBNAILS.clear()
        self.change_page("Unknown Page")
        if auto_refocus:
            self.entry.focus()

    def thread_search(self, user_input: str) -> None:
        "Searches for the given url with threading."
        def search_url(url) -> dict:
            return YouTube.Video.get(url)

        def search_input(query) -> dict:
            return YouTube.VideosSearch(query, limit = 3).result()["result"] #TODO: Set to 10

        next_page = "Unknown Page"
        if searcher.is_playist_url(user_input): #TODO: Check if playlist first before video
            print("Detect playist URL")
        elif searcher.is_video_url(user_input):
            next_page = "Video Details Page"
            self.pages[next_page] = Pages.video_details_page(search_url(user_input))
        else:
            next_page = "Browser Page"
            self.pages[next_page] = Pages.browser_page(search_input(user_input))

        self.change_page(next_page)

    def download(self, video_name, args) -> None:
        "Download to start the downloading process."
        self.clear_entry(False)
        CONST.DOWNLOADER.download(video_name, args)

def get_image(image_name) -> tkinter.PhotoImage:
    "Get an image from the resources folder."
    return tkinter.PhotoImage(file="frontend/images/" + image_name)

def update_downloader() -> None:
    "Manually updates the downloader."
    CONST.DOWNLOADER.update_downloader()

    #TODO: Remove for another type of feedback.
    messagebox.showinfo("Update","exe is manually updated!")

def change_download_location() -> None:
    "Changes the download location of the downloader."
    new_location = filedialog.askdirectory(initialdir=CONST.DOWNLOAD_PATH)
    if new_location != "":
        CONST.DOWNLOAD_PATH = new_location

def switch_autodownload() -> None:
    "This checks if whether to auto update or not"
    with open("resources/update.txt", "w", encoding="utf-8") as file:
        file.write("enabled" if CONST.FRONTEND.autoupdate.get() else "disabled")
