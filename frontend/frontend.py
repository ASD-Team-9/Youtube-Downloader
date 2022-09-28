from turtle import right
import backend.main_download
import customtkinter
import tkinter

colours = {
    "Normal": "#33363B",
    "Normal2": "#292b2f",
    "Dark": "#202225",
    "ButtonNormal": "#36393f",
    "ButtonHover": "#5865f2",
    "Text": "#b9bbbe",
}

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
        self.configure(bg=colours["Normal"])
        self.resizable(False, False)

    def SetLeftFrame(self) -> None:
        third = self.width / 3
        padding = 10
        leftFrameWidth = third - padding * 2

        leftFrame = customtkinter.CTkFrame(self, fg_color=colours["Dark"], corner_radius=0)
        leftFrame.pack(side=tkinter.LEFT, anchor="nw", fill=tkinter.Y, ipadx=padding, ipady=padding)
        self.test = leftFrame

        def SetLeftTopFrame():
            leftTopFrame = customtkinter.CTkFrame(leftFrame, fg_color=colours["Normal2"], height=self.height * 0.1)
            leftTopFrame.pack(side=tkinter.TOP, anchor="nw", fill=tkinter.X, padx=padding, pady=padding, ipady=padding)
            
            logo = GetImage("Download.png").subsample(2)

            self.entry = customtkinter.CTkEntry(leftTopFrame, width=leftFrameWidth - logo.width() - 61, height=40, placeholder_text="Search")
            self.entry.pack(side="left", padx=(padding, 0))
            self.entry.bind("<Enter>", self.GetClipboard)
            self.entry.bind("<Key>", self.HandleSearchChanged)


            customtkinter.CTkButton(
                leftTopFrame, image=logo,
                width=logo.width() + padding, height=logo.height() + padding,
                fg_color=colours["ButtonNormal"], hover_color=colours["ButtonHover"],
                text="", command=self.Download
            ).pack(side="left", fill=tkinter.X, expand=True, padx=padding)
        SetLeftTopFrame()

        def SetLeftMiddleFrame():
            leftMiddleFrame = customtkinter.CTkFrame(leftFrame, fg_color=colours["Normal2"])
            leftMiddleFrame.pack(side="top", fill=tkinter.BOTH, expand=True, padx=padding)
            self.canvas = tkinter.Canvas(leftMiddleFrame, highlightthickness=0, width=leftFrameWidth - padding * 5)
            scrollbar = customtkinter.CTkScrollbar(leftMiddleFrame, fg_color=colours["Normal2"], command=self.canvas.yview)
            scrollbar.pack(side="right", fill="y", padx=(0, 3))

            self.scrollable_frame = tkinter.Frame(self.canvas, bg=colours["Normal2"])
            self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            self.scrollable_frame.pack(fill="both", expand=True)
            
            self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            self.canvas.configure(yscrollcommand=scrollbar.set, bg=colours["Normal2"])
            self.canvas.pack(side="left", fill="both", expand=True, padx=(padding, 0), pady=padding)
        SetLeftMiddleFrame()

        def SetLeftBottomFrame():
            leftBottomFrame = customtkinter.CTkFrame(leftFrame, fg_color=colours["Normal2"], height=self.height * 0.1)
            leftBottomFrame.pack(anchor="n", fill=tkinter.X, padx=10, pady=10)

            def ImageButtons(master, imageName: str, subsample: int, command) -> None:
                logo = GetImage(imageName).subsample(subsample)
                customtkinter.CTkButton(
                    master, image=logo,
                    width=logo.width() + 10, height=logo.height() + 10,
                    fg_color=colours["ButtonNormal"], hover_color=colours["ButtonHover"],
                    text="", command=command
                ).pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=10, pady=10)
            ImageButtons(leftBottomFrame, "Logo.png", 1, lambda: self.ChangePage("Settings Page")) #Example...
            ImageButtons(leftBottomFrame, "Logo.png", 1, lambda: self.ChangePage("Browser Page"))
            ImageButtons(leftBottomFrame, "Logo.png", 1, lambda: self.ChangePage("Account Page"))
            ImageButtons(leftBottomFrame, "Logo.png", 1, lambda: print("I don't know what page this should be."))
        SetLeftBottomFrame()

    def SetRightFrame(self) -> None:
        rightFrame = customtkinter.CTkFrame(self, fg_color=colours["Normal"], corner_radius=0)
        customtkinter.CTkFrame(rightFrame, height=0, width = self.width * 2 / 3, corner_radius=0).pack(anchor="nw") #fill

        self.pages = {
            "Browser Page": self.GetBrowserPage(rightFrame),
            "Settings Page" : self.GetSettingsPage(rightFrame),
            "Account Page" : self.GetAccountPage(rightFrame),
            "Download Options Page": self.GetDownloadOptionsPage(rightFrame),
            #Add pages here...
            #"Page Name" : methodOfPage(rightFrame)
        }
        self.currentPage = self.pages["Browser Page"]
        self.currentPage.pack(fill="both", expand=True)

        rightFrame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    def ChangePage(self, page) -> None:
        self.currentPage.forget()
        self.currentPage = self.pages[page]
        self.currentPage.pack(fill="both", expand=True)

    def GetBrowserPage(self, rightFrame) -> customtkinter.CTkFrame:
        page = customtkinter.CTkFrame(rightFrame, corner_radius=0)

        ###Fill stuff in over here!
        title = customtkinter.CTkLabel(page, text="Browser Page", fg_color=colours["Text"])
        title.pack(anchor="nw", padx=10, pady=10)
        ###

        return page

    def GetSettingsPage(self, rightFrame) -> customtkinter.CTkFrame:
        page = customtkinter.CTkFrame(rightFrame, corner_radius=0)

        ###Fill stuff in over here!
        title = customtkinter.CTkLabel(page, text="Settings Page", fg_color=colours["Text"])
        title.pack(anchor="nw", padx=10, pady=10)
        ###

        return page

    def GetAccountPage(self, rightFrame) -> customtkinter.CTkFrame:
        page = customtkinter.CTkFrame(rightFrame, corner_radius=0)

        ###Fill stuff in over here!
        title = customtkinter.CTkLabel(page, text="Account Page", fg_color="#321321")
        title.pack(anchor="nw", padx=10, pady=10)
        ###

        return page

    def GetDownloadOptionsPage(self, rightFrame) -> customtkinter.CTkFrame:
        page = customtkinter.CTkFrame(rightFrame, corner_radius=0)

        ###Fill stuff in over here!
        title = customtkinter.CTkLabel(page, text="Fetch Youtube Video title", fg_color=colours["Text"])
        title.pack(anchor="nw", padx=10, pady=10)
        ###

        return page

    def GetClipboard(self, event): #This is used as a delegate, the event parameter is needed.
        try:
            self.entry.delete(0, tkinter.END)
            self.entry.insert(0, self.clipboard_get())
        except:
            pass

    def HandleSearchChanged(self, event):
        text = self.entry.get() + event.char
        print("Handle Search Change: " + text)
        if len(self.entry.get()) == 0:
            print("Empty text")
            self.ChangePage("Browser Page")
            return

        if text != "":
            print("Have text")
            self.ChangePage("Download Options Page")
        


    def Download(self):
        value = self.entry.get()
        if value != "":
            self.entry.delete(0, tkinter.END)
            self.downloader.download(value)

        #When adding a new item to the queue. Move this later.
        padding = 10
        width = self.canvas.winfo_width() - 27
        frame = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color=colours["Normal"])
        frame.pack(ipadx=padding, ipady=padding, pady=(0, padding))
        customtkinter.CTkLabel(frame, text="Video Name here", width=width).pack(anchor="n", pady=padding)
        customtkinter.CTkProgressBar(frame, width=width).pack(side="top")

def GetImage(imageName) -> tkinter.PhotoImage:
    return tkinter.PhotoImage(file="frontend/images/" + imageName)
