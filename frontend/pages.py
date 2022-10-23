"Pages for the main frontend class."
from tkinter import messagebox
import tkinter
from urllib.request import urlopen
from io import BytesIO
from PIL import Image, ImageTk
import customtkinter
import youtubesearchpython as YouTube

import backend.constant_variables as CONST
import frontend.frontend as Frontend
import frontend.color as COLOR

class Thumbnail:
    """
    Thumbnail class\n
    Needed to prevent Python garbage collection from removing images loaded from net.
    """
    def __init__(self, url, size = (0, 0)) -> None:
        self.thumbnail2 = None
        try:
            with urlopen(url) as raw_data:
                self.image = Image.open(BytesIO(raw_data.read()))
                self.thumbnail = ImageTk.PhotoImage(
                    self.image.resize(size) if size != (0, 0) else self.image
                )
            CONST.THUMBNAILS.append(self)
            self.index = len(CONST.THUMBNAILS) - 1
        except Exception:
            pass

    def secondary_size(self, size):
        "Create a second size for the thumbnail."
        if self.thumbnail2 is None:
            self.thumbnail2 = ImageTk.PhotoImage(self.image.resize(size))

class Video:
    "Video class\nNeeded to store necessary information."

    def __init__(self, scrollable_frame, video, page_ref) -> None:
        self.page = page_ref
        self.link = video["link"]

        self.frame = customtkinter.CTkFrame(
            scrollable_frame,
            fg_color=COLOR.get_colour("Dark")
        )

        self.thumbnail = CONST.THUMBNAILS[-1]
        image = customtkinter.CTkLabel(
            self.frame, image=self.thumbnail.thumbnail,
        )
        image.pack(side="left", padx=5)
        image.bind("<Button-1>", self.go_to_details_page)

        customtkinter.CTkLabel(
            self.frame, text_color=COLOR.get_colour("Text"),
            text=f"{max_string(video['title'], 70)}\nDuration: {video['duration']}",
            width=CONST.FRONTEND.width*2/3-250, #To hold the width otherwise pack will shrink it
            justify="left", anchor="w"
        ).pack(side="top", anchor="nw", pady=5)

        customtkinter.CTkButton(
            self.frame, command=self.go_to_details_page,
            text="Download",
            fg_color=COLOR.get_colour("ButtonNormal"),
            hover_color=COLOR.get_colour("ButtonHover"),
            text_color=COLOR.get_colour("Text"),
        ).pack(side="bottom", anchor="sw", pady=5)

        self.frame.pack(side="top", pady=2.5, ipady=5, ipadx=5, padx=5)

    def go_to_details_page(self):
        "Switches to video details page with the corresponding link"
        CONST.FRONTEND.pages["Video Details Page"] = video_details_page(
            YouTube.Video.get(self.link), self,
        )
        CONST.FRONTEND.change_page("Video Details Page")

def _get_page_template() -> customtkinter.CTkFrame:
    "Returns an empty template of the page."
    return customtkinter.CTkFrame(
        CONST.FRONTEND.right_frame, corner_radius=0, fg_color=COLOR.get_colour("Normal")
    )

def settings_page() -> customtkinter.CTkFrame:
    "The settings page for the frontend."
    page = _get_page_template()

    CONST.FRONTEND.autoupdate = customtkinter.CTkCheckBox(
        page, text="Enable Auto Update",
        text_color=COLOR.get_colour("Text"),
        command=Frontend.switch_autodownload)
    CONST.FRONTEND.autoupdate.pack(anchor="nw", padx=10, pady=20)

    with open("resources/update.txt", "r", encoding="utf-8") as file:
            if file.readline() == "enabled":
                CONST.FRONTEND.autoupdate.select()

    updatebutton = customtkinter.CTkButton(
        page, text="Update", command=Frontend.update_downloader,
        fg_color=COLOR.get_colour("ButtonNormal"),
        text_color=COLOR.get_colour("Text")
    )
    updatebutton.pack(anchor="nw", padx=20, pady=20)

    change_location = customtkinter.CTkButton(
        page, text="Change Download Location",
        command = Frontend.change_download_location,
        fg_color = COLOR.get_colour("ButtonNormal"), text_color=COLOR.get_colour("Text")
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
        page, text = "Create Account",
        command = lambda: CONST.FRONTEND.ChangePage("New Account Page"),
        fg_color = COLOR.get_colour("ButtonNormal"),
        hover_color = COLOR.get_colour("ButtonHover"), text_color=COLOR.get_colour("Text")
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

    canvas = tkinter.Canvas(
        page, highlightthickness=0,
        bg=COLOR.get_colour("Normal2")
    )

    scrollbar = customtkinter.CTkScrollbar(
        page,
        fg_color=COLOR.get_colour("Normal2"),
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y", padx=(0, 3))

    scrollable_frame = tkinter.Frame(canvas, bg=COLOR.get_colour("Normal"))
    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    scrollable_frame.pack(expand=True, fill="both")

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all(
        "<MouseWheel>",
        lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    )
    canvas.pack(expand=True, fill="both")

    for video in search_results:
        Thumbnail(video["thumbnails"][-1]['url'], (200, 100))
        Video(scrollable_frame, video, page)

    return page

def video_details_page(
        video_details: dict,
        video: Video = None
    ) -> customtkinter.CTkFrame:
    "The video details page for the front end."

    page = _get_page_template()

    top_bar = customtkinter.CTkFrame(
        page, fg_color=COLOR.get_colour("Dark")
    )
    top_bar.pack(fill="x", expand=True, side="top", padx=10, ipady=10)

    if video is not None:
        CONST.FRONTEND.pages["Browser Page"] = video.page
        customtkinter.CTkButton(
            top_bar, command=lambda: CONST.FRONTEND.change_page("Browser Page"),
            text="Back",
            fg_color=COLOR.get_colour("ButtonNormal"),
            hover_color=COLOR.get_colour("ButtonHover"),
            text_color=COLOR.get_colour("Text"),
        ).pack(side="left", padx=(5, 0))

    customtkinter.CTkLabel(
        top_bar, text=max_string(video_details["title"], 60),
        text_color=COLOR.get_colour("Text"),
        text_font=('Helvetica bold', 15)
    ).pack(side="left", padx=(5, 0))

    if video is None:
        Thumbnail(video_details["thumbnails"][-1]["url"], (640, 480))
        nail = CONST.THUMBNAILS[-1].thumbnail
    else:
        video.thumbnail.secondary_size((640, 480))
        nail = CONST.THUMBNAILS[video.thumbnail.index].thumbnail2

    thumbnail = customtkinter.CTkLabel(
        page, image=nail, text_color=COLOR.get_colour("Text")
    )
    thumbnail.pack(side="top")

    # Download Type Dropdown
    download_option = customtkinter.StringVar()
    download_options_menu = customtkinter.CTkOptionMenu(
        page, variable=download_option,
        values=['Best Video', 'Best Audio', 'mp4', 'mp3'],
        text_color=COLOR.get_colour("Text")
    )
    download_options_menu.set('mp4')
    download_options_menu.pack(side="top", padx=10, pady=10)

    def on_download_option_changed(*args):
        # Best video/audio doesn't need quality options
        # Hide it when best _ is selected
        match download_option.get():
            case 'Best Video' | 'Best Audio':
                quality_options_menu.pack_forget()
            case _:
                quality_options_menu.pack(side="top", padx=10, pady=10)
    download_option.trace_variable('w', on_download_option_changed)

    # Quality Dropdown Options
    quality_option = customtkinter.StringVar()
    quality_options_menu = customtkinter.CTkOptionMenu(
        page, variable=quality_option,
        values=['Highest', 'Normal', 'Lowest'],
        text_color=COLOR.get_colour("Text")
    )
    quality_options_menu.set('Highest')
    quality_options_menu.pack(side="top", padx=10, pady=10)

    def download() -> None:
        CONST.DOWNLOADER.download(
            video_details,format_type = download_option.get(), quality_type = quality_option.get()
        )

    image = Frontend.get_image("Download.png")
    customtkinter.CTkButton(
        page, text="Download", image=image, compound="top",
        width=image.width() + 10, height=image.height() + 10,
        fg_color=COLOR.get_colour("ButtonHover"),
        hover_color=COLOR.get_colour("ButtonHover2"),
        text_color=COLOR.get_colour("Text"),
        command=download
    ).pack(side="bottom", anchor="s", fill=customtkinter.X)

    return page

def max_string(string: str, max_char: int):
    "Returns the given string limited to the max character specified"
    return string[:max_char] + ("" if len(string) <= max_char else "...")
