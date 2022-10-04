import backend.global_variables as vars
import backend.main_download
import frontend.pages as Pages
import backend.search as searcher

# UI
import customtkinter
import tkinter
from tkinter import filedialog
from tkinter import messagebox

# Services
import youtubesearchpython as YouTube
import threading

class FrontEnd(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.downloader = backend.main_download.Downloader(self)
        vars.singleton = self
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
        self.test = leftFrame

        def SetLeftTopFrame():
            leftTopFrame = customtkinter.CTkFrame(leftFrame, fg_color=vars.colours["Normal2"], height=self.height * 0.1)
            leftTopFrame.pack(side=tkinter.TOP, anchor="nw", fill=tkinter.X, padx=padding, pady=padding, ipady=padding)

            self.entry = customtkinter.CTkEntry(leftTopFrame, width=leftFrameWidth - 134, height=40, placeholder_text="Search")
            self.entry.pack(side="left", padx=(padding, 0))
            self.entry.bind("<Enter>", self.AutoSearch)
            self.entry.bind("<Return>", self.SearchEntry)

            clearIcon = GetImage("ClearIcon.png").subsample(4)
            searchIcon = GetImage("SearchIcon.png").subsample(3)
            width = ((clearIcon.width() + searchIcon.width()) * 0.5) + padding
            height = ((clearIcon.height() + searchIcon.height()) * 0.5) + padding
            customtkinter.CTkButton(
                leftTopFrame, image=clearIcon, width=width, height=height,
                fg_color=vars.colours["ButtonNormal"], hover_color=vars.colours["ButtonHover"],
                text="", command=self.ClearEntry
            ).pack(side="left", fill=tkinter.X, expand=True, padx=(padding, 0))

            customtkinter.CTkButton(
                leftTopFrame, image=searchIcon, width=width, height=height,
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
            self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
            self.canvas.pack(side="left", fill="both", expand=True, padx=(padding, 0), pady=padding)
        SetLeftMiddleFrame()

        def SetLeftBottomFrame():
            leftBottomFrame = customtkinter.CTkFrame(leftFrame, fg_color=vars.colours["Normal2"], height=self.height * 0.1)
            leftBottomFrame.pack(anchor="n", fill=tkinter.X, padx=10, pady=10)

            def ImageButtons(imageName: str, subsample: int, command) -> None:
                logo = GetImage(imageName).subsample(subsample)
                customtkinter.CTkButton(
                    leftBottomFrame, image=logo,
                    width=logo.width() + 10, height=logo.height() + 10,
                    fg_color=vars.colours["ButtonNormal"], hover_color=vars.colours["ButtonHover"],
                    text="", command=command
                ).pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=10, pady=10)
            ImageButtons("SettingsIcon.png", 3, lambda: self.ChangePage("Settings Page")) #Example...
            ImageButtons("Logo.png", 83, lambda: self.ChangePage("Account Page"))
        SetLeftBottomFrame()

    def SetRightFrame(self) -> None:
        self.rightFrame = customtkinter.CTkFrame(self, fg_color=vars.colours["Normal"], corner_radius=0)
        customtkinter.CTkFrame(self.rightFrame, height=0, width = self.width * 2 / 3, corner_radius=0).pack(anchor="nw") #fill

        self.pages = {
            "Settings Page" : Pages.GetSettingsPage(self),
            "Account Page" : Pages.GetAccountPage(self),
            "Unknown Page" : customtkinter.CTkFrame(self.rightFrame, corner_radius=0, fg_color=vars.colours["Normal"])
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
            if clipboard != self.entry.get() and searcher.isVideoURL(clipboard):
                self.ClearEntry()
                self.entry.insert(0, clipboard)
                self.SearchEntry()

    def ClearEntry(self, autoRefocus = True):
        self.entry.delete(0, tkinter.END)
        self.focus()
        vars.thumbnails.clear()
        self.ChangePage("Unknown Page")
        if (autoRefocus):
            self.entry.focus()

    def SearchEntry(self, event = None):
        search = self.entry.get()
        if search != "":
            vars.threads["searching thread"] = threading.Thread(target=self.thread_search, args=[search])
            vars.threads["searching thread"].start()

    def thread_search(self, userInput):
        nextPage = None
        try:
            if searcher.isVideoURL(userInput):
                nextPage = "Video Details Page"
                self.pages[nextPage] = Pages.GetVideoDetailsPage(self, False, searchURL(userInput))
            elif searcher.isPlayistURL(userInput):
                print("Detect playist URL")
            else:
                raise
        except:
            nextPage = "Browser Page"
            self.pages[nextPage] = Pages.GetBrowserPage(self, searchInput(userInput))
        self.ChangePage(nextPage)
        vars.threads["searching thread"] = None

    def Download(self, video_name, args):
        self.ClearEntry(False)
        self.downloader.download(video_name, args)

def GetImage(imageName) -> tkinter.PhotoImage:
    return tkinter.PhotoImage(file="frontend/images/" + imageName)

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

def updatedownloader():
    vars.singleton.downloader.auto_update()
    messagebox.showinfo("Update","exe is manually updated!")

def changeDownloadLocation():
    newLocation = tkinter.filedialog.askdirectory(initialdir=vars.dowloadLocation)
    if(newLocation != ""):
        vars.dowloadLocation = newLocation
        print("Download Location is: " + vars.dowloadLocation)

    return
def changeColour(choice):
    vars.changeColourSet(choice)
    print("colour set to: "+choice)
    print(vars.colours["ButtonNormal"])
    return
