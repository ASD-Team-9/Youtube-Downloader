import backend.global_variables as vars
import customtkinter

def GetSettingsPage(rightFrame) -> customtkinter.CTkFrame:
    page = customtkinter.CTkFrame(rightFrame, corner_radius=0)

    ###Fill stuff in over here!
    title = customtkinter.CTkLabel(page, text="Settings Page", fg_color=vars.colours["Text"])
    title.pack(anchor="nw", padx=10, pady=10)
    ###
    return page

def GetAccountPage(rightFrame) -> customtkinter.CTkFrame:
    page = customtkinter.CTkFrame(rightFrame, corner_radius=0)

    ###Fill stuff in over here!
    title = customtkinter.CTkLabel(page, text="Account Page", fg_color="#321321")
    title.pack(anchor="nw", padx=10, pady=10)
    ###
    return page

def GetBrowserPage(rightFrame, searchResults) -> customtkinter.CTkFrame:
    page = customtkinter.CTkFrame(rightFrame, corner_radius=0)

    for video in searchResults:
        for key in ["title", "duration", "thumbnails", "link"]:
            title = customtkinter.CTkLabel(page, text=f"{key}: {video[key]}", fg_color=vars.colours["Text"])
            title.pack(anchor="nw", padx=10, pady=10)
    return page

def GetVideoDetailsPage(rightFrame, videoDetails) -> customtkinter.CTkFrame:
    page = customtkinter.CTkFrame(rightFrame, corner_radius=0)
    
    title = customtkinter.CTkLabel(page, text=videoDetails["title"], fg_color="#321321")
    title.pack(anchor="nw", padx=10, pady=10)
    ###

    # # DOWNLOAD TYPE OPTIONS
    # self.downloadOptions = ['mp4', 'mp3']
    # self.downloadOption_var = tkinter.StringVar(self)
    # def downloadOptionChanged(*args):
    #     print("Download Option Change" + self.downloadOption_var.get())
    # downloadOptionsBar = customtkinter.CTkOptionMenu(page, variable=self.downloadOption_var, values=self.downloadOptions, command=downloadOptionChanged)
    # downloadOptionsBar.set('mp4')
    # downloadOptionsBar.pack(anchor="nw", padx=10, pady=10)

    # # D
    # self.videoQualityOptions = ['1080p', '720p', '480p', '360p']
    # self.videoQualityOption_var = tkinter.StringVar(self)
    # def videoQualityChanged(*args):
    #     print("Quality change" + self.videoQualityOption_var.get())
    # videoQualityOptionsBar = customtkinter.CTkOptionMenu(page, variable=self.videoQualityOption_var, values=self.videoQualityOptions, command=videoQualityChanged)
    # videoQualityOptionsBar.set('1080p')
    # videoQualityOptionsBar.pack(anchor="nw", padx=10, pady=10) 

    return page