import customtkinter
import tkinter

colours = {
    "Normal": "#33363B",
    "Normal2": "#292b2f",
    "Dark": "#202225",
    "ButtonNormal": "#36393f",
    "ButtonHover": "#5865f2",
}

class FrontEnd(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()
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
        #
        customtkinter.CTkEntry(leftFrame, width=leftFrameWidth, height=40, placeholder_text="Search").pack(anchor="n", pady=10)
        self.downloadBox = tkinter.Listbox(leftFrame, bg=colours["Normal2"], bd=0, highlightthickness=0).pack(fill=tkinter.BOTH, expand=True, padx=10)

        leftBottomFrame = customtkinter.CTkFrame(leftFrame, fg_color=colours["Normal2"], height=self.height * 0.1)
        ##
        BottomLeftIcons(leftBottomFrame, "frontend/images/Logo.png", 4, lambda: self.ChangePage("Settings Page")) #Example...
        BottomLeftIcons(leftBottomFrame, "frontend/images/Logo.png", 4, lambda: self.ChangePage("Browser Page"))
        BottomLeftIcons(leftBottomFrame, "frontend/images/Logo.png", 4, lambda: print("I don't know what page this should be."))
        BottomLeftIcons(leftBottomFrame, "frontend/images/Logo.png", 4, lambda: print("I don't know what page this should be."))
        ##
        leftBottomFrame.pack(anchor="n", fill=tkinter.X, padx=10, pady=10)
        #
        leftFrame.pack(side=tkinter.LEFT, anchor="nw", fill=tkinter.Y, expand=True, ipadx=10, ipady=10)

    def SetRightFrame(self) -> None:
        rightFrame = customtkinter.CTkFrame(self, fg_color=colours["Normal"], corner_radius=0)
        customtkinter.CTkFrame(rightFrame, height=0, width = self.width * 2 / 3, corner_radius=0).pack(anchor="nw") #fill

        self.pages = {
            "Browser Page": self.GetBrowserPage(rightFrame),
            "Settings Page" : self.GetSettingsPage(rightFrame),
        }
        self.currentPage = self.pages["Browser Page"]
        self.currentPage.pack(fill="both", expand=True)

        rightFrame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    def ChangePage(self, page) -> None:
        self.currentPage.forget()
        self.currentPage = self.pages[page]
        self.currentPage.pack(fill="both", expand=True)

    def GetBrowserPage(self, rightFrame) -> customtkinter.CTkFrame:
        page = customtkinter.CTkFrame(rightFrame)

        ###Fill stuff in over here!
        title = customtkinter.CTkLabel(page, text="Browser Page", fg_color="#321321")
        title.pack(anchor="nw", padx=10, pady=10)
        ###

        return page

    def GetSettingsPage(self, rightFrame) -> customtkinter.CTkFrame:
        page = customtkinter.CTkFrame(rightFrame)

        ###Fill stuff in over here!
        title = customtkinter.CTkLabel(page, text="Settings Page", fg_color="#321321")
        title.pack(anchor="nw", padx=10, pady=10)
        ###

        return page

def BottomLeftIcons(master, imageFile: str, subsample: int, command) -> None:
    logo = tkinter.PhotoImage(file=imageFile)
    logo = logo.subsample(subsample)
    customtkinter.CTkButton(
        master, image=logo,
        width=logo.width() + 10, height=logo.height() + 10,
        fg_color=colours["ButtonNormal"], hover_color=colours["ButtonHover"],
        text="", command=command
    ).pack(side=tkinter.LEFT, fill=tkinter.X, expand=True, padx=10, pady=10)

if __name__ == "__main__":
    FrontEnd()