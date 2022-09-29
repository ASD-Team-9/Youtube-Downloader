import backend.global_variables as vars
import backend.main_download
import frontend.pages as Pages

# UI
import customtkinter
import tkinter
from PIL import Image, ImageTk

# Services
import youtubesearchpython as YouTube
from urllib.request import urlopen
from io import BytesIO
import threading

class FrontEnd(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.downloader = backend.main_download.Downloader(self)
        self.SetMainSettings()
        self.SetLeftFrame()
        self.SetRightFrame()
        self.mainloop()

    def SetMainSettings(self) -> None:
        self.width = 1280
        self.height = 720
        self.geometry(f"{self.width}x{self.height}")
        self.title("YouTube Downloader")
        self.configure(bg=vars.colours["Normal"])
        self.resizable(False, False)

    def SetLeftFrame(self) -> None:
        third = self.width / 3
        padding = 10
        leftFrameWidth = third - padding * 2

        leftFrame = customtkinter.CTkFrame(self, fg_color=vars.colours["Dark"], corner_radius=0)
        leftFrame.pack(side=tkinter.LEFT, anchor="nw", fill=tkinter.Y, ipadx=padding, ipady=padding)

        def SetLeftTopFrame():
            leftTopFrame = customtkinter.CTkFrame(leftFrame, fg_color=vars.colours["Normal2"], height=self.height * 0.1)
            leftTopFrame.pack(side=tkinter.TOP, anchor="nw", fill=tkinter.X, padx=padding, pady=padding, ipady=padding)
            
            logo = GetImage("Download.png").subsample(2)

            self.entry = customtkinter.CTkEntry(leftTopFrame, width=leftFrameWidth - logo.width() - 106, height=40, placeholder_text="Search")
            self.entry.pack(side="left", padx=(padding, 0))
            self.entry.bind("<Enter>", self.AutoSearch)

            customtkinter.CTkButton(
                leftTopFrame, image=logo,
                width=logo.width() + padding, height=logo.height() + padding,
                fg_color=vars.colours["ButtonNormal"], hover_color=vars.colours["ButtonHover"],
                text="", command=self.ClearEntry
            ).pack(side="left", fill=tkinter.X, expand=True, padx=(padding, 0))

            customtkinter.CTkButton(
                leftTopFrame, image=GetImage("Logo.png"),
                width=logo.width() + padding, height=logo.height() + padding,
                fg_color=vars.colours["ButtonNormal"], hover_color=vars.colours["ButtonHover"],
                text="", command=self.SearchEntry
            ).pack(side="left", fill=tkinter.X, expand=True, padx=padding)
        SetLeftTopFrame()

        def SetLeftMiddleFrame():
            leftMiddleFrame = customtkinter.CTkFrame(leftFrame, fg_color=vars.colours["Normal2"])
            leftMiddleFrame.pack(side="top", fill=tkinter.BOTH, expand=True, padx=padding)
            self.canvas = tkinter.Canvas(leftMiddleFrame, highlightthickness=0, width=leftFrameWidth - padding * 5)
            scrollbar = customtkinter.CTkScrollbar(leftMiddleFrame, fg_color=vars.colours["Normal2"], command=self.canvas.yview)
            scrollbar.pack(side="right", fill="y", padx=(0, 3))

            self.scrollable_frame = tkinter.Frame(self.canvas, bg=vars.colours["Normal2"])
            self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            self.scrollable_frame.pack(fill="both", expand=True)
            
            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=scrollbar.set, bg=vars.colours["Normal2"])
            self.canvas.pack(side="left", fill="both", expand=True, padx=(padding, 0), pady=padding)
        SetLeftMiddleFrame()

        def SetLeftBottomFrame():
            leftBottomFrame = customtkinter.CTkFrame(leftFrame, fg_color=vars.colours["Normal2"], height=self.height * 0.1)
            leftBottomFrame.pack(anchor="n", fill=tkinter.X, padx=10, pady=10)

            def ImageButtons(master, imageName: str, subsample: int, command) -> None:
                logo = GetImage(imageName).subsample(subsample)
                customtkinter.CTkButton(
                    master, image=logo,
                    width=logo.width() + 10, height=logo.height() + 10,
                    fg_color=vars.colours["ButtonNormal"], hover_color=vars.colours["ButtonHover"],
                    text="", command=command
                ).pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=10, pady=10)
            ImageButtons(leftBottomFrame, "Logo.png", 1, lambda: self.ChangePage("Settings Page")) #Example...
            ImageButtons(leftBottomFrame, "Logo.png", 1, lambda: self.ChangePage("Account Page"))
        SetLeftBottomFrame()

    def SetRightFrame(self) -> None:
        self.rightFrame = customtkinter.CTkFrame(self, fg_color=vars.colours["Normal"], corner_radius=0)
        customtkinter.CTkFrame(self.rightFrame, height=0, width = self.width * 2 / 3, corner_radius=0).pack(anchor="nw") #fill

        self.pages = {
            "Settings Page" : Pages.GetSettingsPage(self.rightFrame),
            "Account Page" : Pages.GetAccountPage(self.rightFrame),
            #Add pages here...
            #"Page Name" : methodOfPage(rightFrame)
        }
        self.currentPage = None

        self.rightFrame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    def ChangePage(self, page) -> None:
        if (self.currentPage != None):
            self.currentPage.forget()
        self.currentPage = self.pages[page]
        self.currentPage.pack(fill="both", expand=True)

    def AutoSearch(self, event): #The event parameter is needed.
        if vars.threads["searching thread"] == None:
            clipboard = self.clipboard_get()
            if clipboard != self.entry.get() and vars.regex.fullmatch(clipboard):
                self.ClearEntry()
                self.entry.insert(0, clipboard)
                self.SearchEntry()

    def ClearEntry(self):
        self.entry.delete(0, tkinter.END)
        self.focus()
        self.entry.focus()

    def SearchEntry(self):
        vars.threads["searching thread"] = threading.Thread(target=self.thread_search, args=[self.entry.get()])
        vars.threads["searching thread"].start()

    def thread_search(self, userInput):
        nextPage = None
        try:
            if vars.regex.fullmatch(userInput):
                nextPage = "Video Details Page"
                self.pages[nextPage] = Pages.GetVideoDetailsPage(self.rightFrame, searchURL(userInput))
            else:
                raise
        except:
            nextPage = "Browser Page"
            self.pages[nextPage] = Pages.GetBrowserPage(self.rightFrame, searchInput(userInput))
        self.ChangePage(nextPage)
        vars.threads["searching thread"] = None

    def Download(self):
        value = self.entry.get()
        if value != "":
            self.entry.delete(0, tkinter.END)
            self.downloader.download(value)

        #When adding a new item to the queue. Move this later.
        padding = 10
        width = self.canvas.winfo_width() - 27
        frame = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=vars.colours["Normal"])
        frame.pack(ipadx=padding, ipady=padding, pady=(0, padding))
        customtkinter.CTkLabel(frame, text="Video Name here", width=width).pack(anchor="n", pady=padding)
        customtkinter.CTkProgressBar(frame, width=width).pack(side="top")

def GetImage(imageName) -> tkinter.PhotoImage:
    return tkinter.PhotoImage(file="frontend/images/" + imageName)

def GetImageFromURL(url) -> tkinter.PhotoImage:
    try:
        u = urlopen(url)
        raw_data = u.read()
        u.close()
        return ImageTk.PhotoImage(Image.open(BytesIO(raw_data)))
    except:
        return

def searchURL(url):
    try:
        return YouTube.Video.get(url)
    except:
        return

def searchInput(query):
    try:
        videosSearch = YouTube.VideosSearch(query, limit = 20)
        return videosSearch.result()["result"]
    except:
        return