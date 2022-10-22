"Pages for the main frontend class."
from tkinter import messagebox
from urllib.request import urlopen
from io import BytesIO

from PIL import Image, ImageTk
import customtkinter

import backend.constant_variables as CONST
import frontend.frontend as Frontend

def _get_page_template() -> customtkinter.CTkFrame:
    "Returns an empty template of the page."
    return customtkinter.CTkFrame(
        CONST.FRONTEND.right_frame, corner_radius=0, fg_color=CONST.get_colour("Normal")
    )

def settings_page() -> customtkinter.CTkFrame:
    "The settings page for the frontend."
    page = _get_page_template()
    autoupdate = customtkinter.CTkCheckBox(page, text="Enable Auto Update")
    autoupdate.pack(anchor="nw", padx=10, pady=20)
    autoupdate.select() #TODO: Make this dynamic with login

    updatebutton = customtkinter.CTkButton(
        page, text="Update", command=Frontend.update_downloader,
        fg_color=CONST.get_colour("ButtonNormal")
    )
    updatebutton.pack(anchor="nw", padx=20, pady=20)

    change_location = customtkinter.CTkButton(
        page, text="Change Download Location",
        command = Frontend.change_download_location, fg_color=CONST.get_colour("ButtonNormal")
    )
    change_location.pack(anchor="nw", padx=20, pady=20)

    colour_choice_label = customtkinter.CTkLabel(page, text="Choose Colour Scheme:")
    colour_choice_label.pack(anchor="nw", padx=20, pady=20)

    colour_choice = customtkinter.CTkOptionMenu(
        page, values=["Normal", "Green"]
    )
    colour_choice.pack(anchor="nw", padx=20, pady=10)
    colour_choice.set("Normal")
    return page

def history_page() -> customtkinter.CTkFrame:
    "The history page"
    page = _get_page_template()

    title = customtkinter.CTkLabel(page, text="History Page", fg_color="#321321")
    title.pack(anchor="nw", padx=10, pady=10)

    return page

def account_page() -> customtkinter.CTkFrame:
    "The account page for the frontend."

    def login() -> None:
        while True:
            usernameInput = username.get()
            passwordInput = password.get()
            with open("resources/logins.txt", "r", encoding="utf-8") as accounts_file:
                for line in accounts_file:
                    usernameLogin, passwordLogin = line.replace("\n","").split("|")
                    if usernameInput == usernameLogin and passwordInput == passwordLogin:
                        messagebox.showinfo("Login","Login is successful")
                        #TODO: Remove this and just log in, hook this up to a new page.
                        CONST.FRONTEND.change_page("History Page")
                        break
                else:
                    messagebox.showinfo("Login","Login unsuccessful try again")
                    break
                break

    page = _get_page_template()

    login_page = customtkinter.CTkLabel(page, text="Login Page", fg_color="#321321")
    login_page.pack(anchor="nw", padx=10, pady=10)

    username = customtkinter.CTkEntry(page, placeholder_text="Username")
    username.pack(side="top",anchor="nw", padx=10)
    username.bind("<Return>", login)

    password = customtkinter.CTkEntry(page, placeholder_text="Password", show="*")
    password.pack(side="top",anchor="nw", padx=10,pady=10)
    password.bind("<Return>", login)

    login_button = customtkinter.CTkButton(
        page, text="Login", command=login,
        fg_color=CONST.get_colour("ButtonNormal"), hover_color=CONST.get_colour("ButtonHover")
    )
    login_button.pack(side="top",anchor="nw", padx=10)

    create_account_button = customtkinter.CTkButton(
        page, text="Create Account",
        command=lambda: CONST.FRONTEND.change_page("New Account Page"),
        fg_color=CONST.get_colour("ButtonNormal"), hover_color=CONST.get_colour("ButtonHover")
    )
    create_account_button.pack(side="top",anchor="nw", padx=10, pady=5)

    return page

def new_account_page() -> customtkinter.CTkFrame:
    "The new account page for the frontend."
    def register():
        username = new_username.get()
        password = new_password.get()
        with open("resources/logins.txt","a", encoding="utf-8") as file:
            file.write('\n'+ username + '|' + password)
            file.close()
        messagebox.showinfo("Create New Account","Account Created!")

    page = _get_page_template()

    title = customtkinter.CTkLabel(page, text="Create a New Account", fg_color="#321321")
    title.pack(anchor="nw", padx=10, pady=10)

    new_username = customtkinter.CTkEntry(page, placeholder_text="New Username")
    new_username.pack(side="top",anchor="nw", padx=10)
    new_username.bind("<Return>", register)

    new_password = customtkinter.CTkEntry(page, placeholder_text="New Password")
    new_password.pack(side="top",anchor="nw", padx=10,pady=10)
    new_password.bind("<Return>", register)

    create_button = customtkinter.CTkButton(
        page, text="Create Account", command=register,
        fg_color=CONST.get_colour("ButtonNormal"),
        hover_color=CONST.get_colour("ButtonHover")
    )
    create_button.pack(side="top",anchor="nw", padx=10)

    return page

def browser_page(search_results: dict) -> customtkinter.CTkFrame:
    "The browser page for the front end."
    page = _get_page_template()

    for video in search_results:
        for key in ["title", "duration", "thumbnails", "link"]:
            title = customtkinter.CTkLabel(
                page, text=f"{key}: {video[key]}", fg_color=CONST.get_colour("Text")
            )
            title.pack(anchor="nw", padx=10, pady=10)
    return page

#TODO: came_from_browser_page implementation
def video_details_page(came_from_browser_page: bool, video_details: dict) -> customtkinter.CTkFrame:
    "The video details page for the front end."
    def download() -> None:
        CONST.FRONTEND.download(
            video_details["title"], [CONST.YTDLP, video_details["link"]] + update_video_args()
        )

    page = _get_page_template()

    customtkinter.CTkLabel(
        page, text=video_details["title"], fg_color="#321321"
    ).pack(anchor="nw", padx=10, pady=10)

    Thumbnail(video_details["thumbnails"][-1]["url"])
    thumbnail = customtkinter.CTkLabel(page, image=CONST.THUMBNAILS[0].thumbnail)
    thumbnail.pack(anchor="nw", side="top")

    # Download Type Dropdown
    download_option = customtkinter.StringVar()
    download_options_menu = customtkinter.CTkOptionMenu(
        page, variable=download_option,
        values=['mp4', 'm4a', 'mp3'],
    )
    download_options_menu.set('mp4')
    download_options_menu.pack(anchor="nw", padx=10, pady=10)

    # Quality Dropdown Options
    quality_option = customtkinter.StringVar()
    quality_options_menu = customtkinter.CTkOptionMenu(
        page, variable=quality_option,
        values=['highest', 'medium', 'low', 'lowest'],
    )
    quality_options_menu.set('highest')
    quality_options_menu.pack(anchor="nw", padx=10, pady=10)

    # Process args for YT-DLP
    def update_video_args() -> None:
        defaualt_args = [
            "-o", f"{CONST.DOWNLOAD_PATH}/%(title)s.%(ext)s",
            "--progress-template",
            "%(progress._percent_str)s %(progress._eta_str)s %(progress._speed_str)s"
        ]

        args = ["-f"]
        match download_option.get():
            case "mp4":
                match quality_option.get():
                    case "highest":
                        args.append("-bestvideo")
                    case "medium":
                        args.append("136")
                    case "low":
                        args.append("135")
                    case "lowest":
                        args.append("160")
            case "m4a":
                args.append("140" if quality_option.get() == "highest" else "139")
            case "mp3":
                #TODO get mp3 with ffmpeg
                pass
        return defaualt_args + args

    image = Frontend.get_image("Download.png")
    customtkinter.CTkButton(
        page, text="Download", image=image, compound="top",
        width=image.width() + 10, height=image.height() + 10,
        fg_color=CONST.get_colour("ButtonHover"), hover_color=CONST.get_colour("ButtonHover2"),
        command=download
    ).pack(side="top", anchor="s", fill=customtkinter.X)

    return page

class Thumbnail:
    """
    Thumbnail class\n
    Needed to prevent Python garbage collection from removing images loaded from net.
    """
    def __init__(self, url) -> None:
        try:
            with urlopen(url) as raw_data:
                self.thumbnail = ImageTk.PhotoImage(Image.open(BytesIO(raw_data.read())))
            CONST.THUMBNAILS.append(self)
        except Exception:
            pass
