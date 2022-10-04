import backend.global_variables as vars
import customtkinter

from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

import frontend.frontend as Frontend

def GetSettingsPage(frontend) -> customtkinter.CTkFrame:
    page = customtkinter.CTkFrame(frontend.rightFrame, corner_radius=0, fg_color=vars.colours["Normal"])

    ###Fill stuff in over here!
    title = customtkinter.CTkLabel(page, text="Settings Page", fg_color=vars.colours["Text"])
    title.pack(anchor="nw", padx=10, pady=10)
    ###
    return page

def GetAccountPage(frontend) -> customtkinter.CTkFrame:
    def login():
        print("Hi this is working")

    page = customtkinter.CTkFrame(frontend.rightFrame, corner_radius=0, fg_color=vars.colours["Normal"])

    ###Fill stuff in over here!
    title = customtkinter.CTkLabel(page, text="Account Page", fg_color="#321321")
    title.pack(anchor="nw", padx=10, pady=10)

    username = customtkinter.CTkEntry(page, placeholder_text="Username")
    username.pack(side="left")
    username.bind("<Return>", login)

    password = customtkinter.CTkEntry(page, placeholder_text="Password")
    password.pack(side="left")
    password.bind("<Return>", login)

    customtkinter.CTkButton(
        page, text="Login", command=login,
        fg_color=vars.colours["ButtonNormal"], hover_color=vars.colours["ButtonHover"]
    ).pack(side="left")
    ###
    return page

def GetBrowserPage(frontend, searchResults) -> customtkinter.CTkFrame:
    page = customtkinter.CTkFrame(frontend.rightFrame, corner_radius=0, fg_color=vars.colours["Normal"])

    for video in searchResults:
        for key in ["title", "duration", "thumbnails", "link"]:
            title = customtkinter.CTkLabel(page, text=f"{key}: {video[key]}", fg_color=vars.colours["Text"])
            title.pack(anchor="nw", padx=10, pady=10)
    return page

def GetVideoDetailsPage(frontend, cameFromBrowserPage, videoDetails) -> customtkinter.CTkFrame:
    page = customtkinter.CTkFrame(frontend.rightFrame, corner_radius=0, fg_color=vars.colours["Normal"])
    
    customtkinter.CTkLabel(page, text=videoDetails["title"], fg_color="#321321").pack(anchor="nw", padx=10, pady=10)

    Thumbnail(videoDetails["thumbnails"][-1]["url"])
    thumbnail = customtkinter.CTkLabel(page, image=vars.thumbnails[0].thumbnail)
    thumbnail.pack(anchor="nw", side="top")

    progressArgs = ["-o", "%(title)s.%(ext)s", "--progress-template", "%(progress._percent_str)s %(progress._eta_str)s %(progress._speed_str)s"]
    ## DOWNLOAD TYPE OPTIONS

    # Download Type Dropdown
    downloadOptions = ['mp4', 'm4a', 'mp3']
    downloadOption_var = customtkinter.StringVar()
    def downloadOptionChanged(*args):
        print("Download Option Change: " + downloadOption_var.get())
        updateQualityArgs()
    downloadOptionsBar = customtkinter.CTkOptionMenu(page, variable=downloadOption_var, values=downloadOptions, command=downloadOptionChanged)
    downloadOptionsBar.set('mp4')
    downloadOptionsBar.pack(anchor="nw", padx=10, pady=10)

    # Quality Dropdown Options
    qualityOptions = ['highest', 'medium', 'low', 'lowest']
    qualityOption_var = customtkinter.StringVar()
    def qualityChanged(*args):
        print("Quality change: " + qualityOption_var.get())
        updateQualityArgs()
    qualityOptionsBar = customtkinter.CTkOptionMenu(page, variable=qualityOption_var, values=qualityOptions, command=qualityChanged)
    qualityOptionsBar.set('highest')
    qualityOptionsBar.pack(anchor="nw", padx=10, pady=10) 

    # Process args for YT-DLP
    def updateQualityArgs():
        qualityArgs = []
        if downloadOption_var.get() == "mp4":
            # if qualityOption_var.get() == "highest": qualityArgs = ["-f", "bestvideo"]
            if qualityOption_var.get() == "medium": qualityArgs = ["-f", "136"]
            elif qualityOption_var.get() == "low" : qualityArgs = ["-f", "135"]
            elif qualityOption_var.get() == "lowest" : qualityArgs = ["-f", "160"]
            else: qualityArgs.append("bestvideo")
        elif downloadOption_var.get() == "m4a":
            if qualityOption_var.get() == "highest": qualityArgs = ["-f", "140"]
            else: qualityArgs = ["-f", "139"]
        elif downloadOption_var.get() == "mp3":
            #TODO get mp3 with ffmpeg
            if qualityOption_var.get() == "highest":  qualityArgs = ["-f", "139"]
            else: qualityArgs = ["-f", "139"]
        
        return qualityArgs

    image = Frontend.GetImage("Download.png")
    customtkinter.CTkButton(
        page, text="Download", image=image, compound="top",
        width=image.width() + 10, height=image.height() + 10,
        fg_color=vars.colours["ButtonHover"], hover_color=vars.colours["ButtonHover2"],
        command=lambda: frontend.Download(videoDetails["title"], [videoDetails["link"]] + progressArgs + updateQualityArgs()) #TODO: Last argument is where you combine all preferences + path + etc.
    ).pack(side="top", anchor="s", fill=customtkinter.X)

    return page

class Thumbnail:
    def __init__(self, url) -> None:
        try:
            u = urlopen(url)
            raw_data = u.read()
            u.close()
            self.thumbnail = ImageTk.PhotoImage(Image.open(BytesIO(raw_data)))
        except:
            return
        vars.thumbnails.append(self)
