"Pages for the main frontend class."
from tkinter import messagebox
from urllib.request import urlopen
from io import BytesIO

from PIL import Image, ImageTk
import customtkinter

import backend.constant_variables as CONST
import backend.format as Format
import frontend.frontend as Frontend
import frontend.color as COLOR

def _get_page_template() -> customtkinter.CTkFrame:
    "Returns an empty template of the page."
    return customtkinter.CTkFrame(
        CONST.FRONTEND.right_frame, corner_radius=0, fg_color=COLOR.get_colour("Normal")
    )

def settings_page() -> customtkinter.CTkFrame:
    "The settings page for the frontend."
    page = _get_page_template()
    autoupdate = customtkinter.CTkCheckBox(page, text="Enable Auto Update", text_color=COLOR.get_colour("Text"))
    autoupdate.pack(anchor="nw", padx=10, pady=20)
    autoupdate.select() #TODO: Make this dynamic with login

    updatebutton = customtkinter.CTkButton(
        page, text="Update", command=Frontend.update_downloader,
        fg_color=COLOR.get_colour("ButtonNormal"),
        text_color=COLOR.get_colour("Text")
    )
    updatebutton.pack(anchor="nw", padx=20, pady=20)

    change_location = customtkinter.CTkButton(
        page, text="Change Download Location",
        command = Frontend.change_download_location, fg_color=COLOR.get_colour("ButtonNormal"), text_color=COLOR.get_colour("Text")
    )
    change_location.pack(anchor="nw", padx=20, pady=20)

    colour_choice_label = customtkinter.CTkLabel(page, text="Choose Colour Scheme:", text_color=COLOR.get_colour("Text"))
    colour_choice_label.pack(anchor="nw", padx=20, pady=20)

    colour_choice = customtkinter.CTkOptionMenu(
        page, values=["Normal", "Green"]
    )
    colour_choice.pack(anchor="nw", padx=20, pady=10)
    colour_choice.set("Normal")
    return page

def account_page() -> customtkinter.CTkFrame:
    "The account page for the frontend."
    def login() -> None:
        with open("resources/logins.txt", "r", encoding="utf-8") as file: #TODO: Make this dynamic
            correct_username = file.readline().strip()
            correct_password = file.readline().strip()
        if correct_username == username.get() and correct_password == password.get():
            #TODO: Remove this and just log in, hook this up to a new page.
            messagebox.showinfo("Login","Login is successful")
            username.destroy()
            password.destroy()
            login_button.destroy()
            create_account_button.destroy()
            new_title = customtkinter.CTkLabel(page, text="Playlists", fg_color="#321321")
            new_title.pack(anchor="nw", padx=10, pady=10)
        else:
            messagebox.showinfo("Login","Login unsuccessful try again")

    page = _get_page_template()

    username = customtkinter.CTkEntry(page, placeholder_text="Username")
    username.pack(side="top",anchor="nw", padx=10)
    username.bind("<Return>", login)

    password = customtkinter.CTkEntry(page, placeholder_text="Password", show="*")
    password.pack(side="top",anchor="nw", padx=10,pady=10)
    password.bind("<Return>", login)

    login_button = customtkinter.CTkButton(
        page, text="Login", command=login, text_color=COLOR.get_colour("Text"),
        fg_color=COLOR.get_colour("ButtonNormal"), hover_color=COLOR.get_colour("ButtonHover")
    )
    login_button.pack(side="top",anchor="nw", padx=10)

    create_account_button = customtkinter.CTkButton(
        page, text="Create Account",
        command=lambda: CONST.FRONTEND.ChangePage("New Account Page"),
        fg_color=COLOR.get_colour("ButtonNormal"), hover_color=COLOR.get_colour("ButtonHover"), text_color=COLOR.get_colour("Text")
    )
    create_account_button.pack(side="top",anchor="nw", padx=10, pady=5)

    return page

def new_account_page() -> customtkinter.CTkFrame:
    "The new account page for the frontend."
    def create_account():
        with open("resources/logins.txt","a", encoding="utf-8") as file:
            file.write(new_username.get() + "\n")
            file.write(new_password.get() + "\n")
        messagebox.showinfo("Create New Account","Account Created!")

    page = _get_page_template()

    title = customtkinter.CTkLabel(page, text="Create a New Account", fg_color="#321321")
    title.pack(anchor="nw", padx=10, pady=10)

    new_username = customtkinter.CTkEntry(page, placeholder_text="New Username")
    new_username.pack(side="top",anchor="nw", padx=10)
    new_username.bind("<Return>", create_account)

    new_password = customtkinter.CTkEntry(page, placeholder_text="New Password")
    new_password.pack(side="top",anchor="nw", padx=10,pady=10)
    new_password.bind("<Return>", create_account)

    create_button = customtkinter.CTkButton(
        page, text="Create Account", command=create_account,
        fg_color=COLOR.get_colour("ButtonNormal"),
        hover_color=COLOR.get_colour("ButtonHover"),
        text_color=COLOR.get_colour("Text")
    )
    create_button.pack(side="top",anchor="nw", padx=10)

    return page

def browser_page(search_results: dict) -> customtkinter.CTkFrame:
    "The browser page for the front end."
    page = _get_page_template()

    for video in search_results:
        for key in ["title", "duration", "thumbnails", "link"]:
            title = customtkinter.CTkLabel(
                page, text=f"{key}: {video[key]}", fg_color=COLOR.get_colour("Text")
            )
            title.pack(anchor="nw", padx=10, pady=10)
    return page

#TODO: came_from_browser_page implementation
def video_details_page(came_from_browser_page: bool, video_details: dict) -> customtkinter.CTkFrame:
    "The video details page for the front end."

    page = _get_page_template()

    customtkinter.CTkLabel(
        page, text=video_details["title"], text_color=COLOR.get_colour("Text"), text_font=('Helvetica bold',30)
    ).pack(anchor="nw", padx=10, pady=10)

    Thumbnail(video_details["thumbnails"][-1]["url"])
    thumbnail = customtkinter.CTkLabel(page, image=CONST.THUMBNAILS[0].thumbnail, text_color=COLOR.get_colour("Text"))
    thumbnail.pack(anchor="nw", side="top")

    # Download Type Dropdown
    download_option = customtkinter.StringVar()
    download_options_menu = customtkinter.CTkOptionMenu(
        page, variable=download_option,
        values=['best video', 'best audio', 'mp4', 'webm', 'm4a', 'mp3'],
        text_color=COLOR.get_colour("Text")
    )
    download_options_menu.set('mp4')
    download_options_menu.pack(anchor="nw", padx=10, pady=10)

    def on_download_option_changed(*args):
        # Best video/audio doesn't need quality options
        # Hide it when best __ is seledted
        match download_option.get():
            case 'best video' | 'best audio':
                quality_options_menu.pack_forget()
            case _:
                quality_options_menu.pack(anchor="nw", padx=10, pady=10)
    download_option.trace_variable('w', on_download_option_changed)

    # Quality Dropdown Options
    quality_option = customtkinter.StringVar()
    quality_options_menu = customtkinter.CTkOptionMenu(
        page, variable=quality_option,
        values=['highest', 'medium', 'low', 'lowest'],
        text_color=COLOR.get_colour("Text")
    )
    quality_options_menu.set('highest')
    quality_options_menu.pack(anchor="nw", padx=10, pady=10)

    def download() -> None:
        CONST.DOWNLOADER.download(
            video_details,format_type = download_option.get(), quality_type = quality_option.get()
        )

    image = Frontend.get_image("Download.png")
    customtkinter.CTkButton(
        page, text="Download", image=image, compound="top",
        width=image.width() + 10, height=image.height() + 10,
        fg_color=COLOR.get_colour("ButtonHover"), hover_color=COLOR.get_colour("ButtonHover2"), 
        text_color=COLOR.get_colour("Text"),
        command=download
    ).pack(side="bottom", anchor="s", fill=customtkinter.X)

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
