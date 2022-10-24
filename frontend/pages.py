"Pages for the main frontend class."
from tkinter import messagebox
import tkinter
from tkinter import filedialog
import os
import os.path
from urllib.request import urlopen
from io import BytesIO
import datetime

from PIL import Image, ImageTk
import customtkinter
import youtubesearchpython as YouTube
from cryptography.fernet import Fernet

from tkVideoPlayer import TkinterVideo
from backend.action_thread import ActionThread

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

class BrowsingVideo:
    "Video class\nNeeded to store necessary information."

    def __init__(self, scrollable_frame, video, page_ref) -> None:
        self.page = page_ref
        self.link = video["link"]
        self.frame, self.thumbnail = _create_video_item(scrollable_frame, video)

        customtkinter.CTkButton(
            self.frame, command=self.go_to_details_page,
            text="Download",
            fg_color=COLOR.get_colour("ButtonNormal"),
            hover_color=COLOR.get_colour("ButtonHover"),
            text_color=COLOR.get_colour("Text"),
        ).pack(side="bottom", anchor="sw", pady=5)

    def go_to_details_page(self):
        "Switches to video details page with the corresponding link"
        CONST.FRONTEND.pages["Video Details Page"] = video_details_page(
            YouTube.Video.get(self.link), self,
        )
        CONST.FRONTEND.change_page("Video Details Page")

class PlaylistVideo:
    "A playlist video for the playlist page"
    def __init__(self, scrollable_frame, video) -> None:
        self.video = video
        self.frame, self.thumbnail = _create_video_item(scrollable_frame, video)

        self.checkbox = customtkinter.CTkCheckBox(
            self.frame,
            text="Download this video",
            text_color=COLOR.get_colour("Text"),
        )
        self.checkbox.select()
        self.checkbox.pack(side="bottom", anchor="sw", pady=5)

    def is_checked(self):
        "Returns true if the checkbox is checked"
        return self.checkbox.get()

def _get_page_template() -> customtkinter.CTkFrame:
    "Returns an empty template of the page."
    return customtkinter.CTkFrame(
        CONST.FRONTEND.right_frame, corner_radius=0, fg_color=COLOR.get_colour("Normal")
    )

def _create_video_item(scrollable_frame, video) -> customtkinter.CTkFrame:
    frame = customtkinter.CTkFrame(
        scrollable_frame,
        fg_color=COLOR.get_colour("Dark")
    )

    thumbnail = Thumbnail(video["thumbnails"][-1]['url'], (200, 100))
    customtkinter.CTkLabel(
        frame, image=thumbnail.thumbnail,
    ).pack(side="left", padx=5)

    customtkinter.CTkLabel(
        frame, text_color=COLOR.get_colour("Text"),
        text=f"{max_string(video['title'], 70)}\nDuration: {video['duration']}",
        width=CONST.FRONTEND.width*2/3-250, #To hold the width otherwise pack will shrink it
        justify="left", anchor="w"
    ).pack(side="top", anchor="nw", pady=5)
    frame.pack(side="top", pady=2.5, ipady=5, ipadx=5, padx=5)
    return frame, thumbnail

def _get_scrollable_frame(page: customtkinter.CTkFrame) -> tkinter.Frame:
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
    return scrollable_frame

def settings_page() -> customtkinter.CTkFrame:
    "The settings page for the frontend."
    page = _get_page_template()

    CONST.FRONTEND.autoupdate = customtkinter.CTkCheckBox(
        page, text="Enable Auto Update",
        text_color=COLOR.get_colour("Text"),
        command=Frontend.switch_auto_update)
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

    colour_choice_label = customtkinter.CTkLabel(
        page, text="Choose Colour Scheme:", text_color=COLOR.get_colour("Text")
    )
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
        if os.path.exists("resources/encryptedLogins.txt"):
            # Reading the key from file
            with open('resources/secretLoginKey.key','rb') as file:
                fernet = Fernet(file.read())

            # Read the encrypted data from file
            with open("resources/encryptedLogins.txt","rb+") as file:
                decrypted_data = fernet.decrypt(file.read()).decode()
                print(decrypted_data)

            for line in decrypted_data.split("\n"):
                details = line.split("|")
                if details[0] == username.get() and details[1] == password.get():
                    CONST.FRONTEND.change_page("History Page")
                    return
            messagebox.showinfo("Login","Login unsuccessful try again")

    page = _get_page_template()

    login_page = customtkinter.CTkLabel(page, text="Login Page", fg_color="#321321")
    login_page.pack(anchor="nw", padx=10, pady=10)

    username = customtkinter.CTkEntry(page, placeholder_text="Username")
    username.pack(side="top",anchor="nw", padx=10)
    username.bind("<Return>", lambda e: login())

    password = customtkinter.CTkEntry(page, placeholder_text="Password", show="*")
    password.pack(side="top",anchor="nw", padx=10,pady=10)
    password.bind("<Return>", lambda e: login())

    login_button = customtkinter.CTkButton(
        page, text="Login", command=login, text_color=COLOR.get_colour("Text"),
        fg_color=COLOR.get_colour("ButtonNormal"), hover_color=COLOR.get_colour("ButtonHover")
    )
    login_button.pack(side="top",anchor="nw", padx=10)

    create_account_button = customtkinter.CTkButton(
        page, text="Create Account",command=lambda:
        CONST.FRONTEND.change_page("New Account Page"),
        fg_color=COLOR.get_colour("ButtonNormal"), hover_color=COLOR.get_colour("ButtonHover")
    )
    create_account_button.pack(side="top",anchor="nw", padx=10)

    video_player_button = customtkinter.CTkButton(
        page, text="Video Player", command=video_player,
        fg_color=COLOR.get_colour("ButtonNormal"), hover_color=COLOR.get_colour("ButtonHover")
    )
    video_player_button.pack(side="top",anchor="nw", padx=10)

    return page

def new_account_page() -> customtkinter.CTkFrame:
    "The new account page for the frontend."
    def register():
        username = new_username.get()
        password = new_password.get()

        # Read the key from file
        with open('resources/secretLoginKey.key','rb') as file:
            fernet = Fernet(file.read())

        # Read the encrypted data from file
        with open("resources/encryptedLogins.txt","rb+") as file:
            decrypted_data = fernet.decrypt(file.read()).decode()
            decrypted_data += f"\n{username}|{password}"
            if CONST.AZURE_TEST:
                print(decrypted_data)

        with open("resources/encryptedLogins.txt","wb") as file:
            file.write(fernet.encrypt(decrypted_data.encode()))
        CONST.FRONTEND.change_page("Account Page")

    page = _get_page_template()

    title = customtkinter.CTkLabel(page, text="Create a New Account", fg_color="#321321")
    title.pack(anchor="nw", padx=10, pady=10)

    new_username = customtkinter.CTkEntry(page, placeholder_text="New Username")
    new_username.pack(side="top",anchor="nw", padx=10)
    new_username.bind("<Return>", lambda e: register())

    new_password = customtkinter.CTkEntry(page, placeholder_text="New Password")
    new_password.pack(side="top",anchor="nw", padx=10,pady=10)
    new_password.bind("<Return>", lambda e: register())

    create_button = customtkinter.CTkButton(
        page, text="Create Account", command=register,
        fg_color=COLOR.get_colour("ButtonNormal"),
        hover_color=COLOR.get_colour("ButtonHover")
    )
    create_button.pack(side="top",anchor="nw", padx=10)

    return page

def video_player():
    "Video Player page."
    page = _get_page_template()

    def update_duration(event):
        """ updates the duration after finding the duration """
        duration = vid_player.video_info()["duration"]
        end_time["text"] = str(datetime.timedelta(seconds=duration))
        progress_slider["to"] = duration


    def update_scale(event):
        """ updates the scale value """
        progress_slider.set(vid_player.current_duration())


    def load_video():
        """ loads the video """
        file_path = filedialog.askopenfilename(filetypes=[
                       ('Video Files', ["*.mp4"])])

        if file_path:
            vid_player.load(file_path)

            progress_slider.config(to=0, from_=0)
            play_pause_btn["text"] = "Play"
            progress_slider.set(0)


    def seek(event=None):
        """ used to seek a specific timeframe """
        vid_player.seek(int(progress_slider.get()))


    def skip(value: int):
        """ skip seconds """
        vid_player.seek(int(progress_slider.get())+value)
        progress_slider.set(progress_slider.get() + value)


    def play_pause():
        """ pauses and plays """
        if vid_player.is_paused():
            vid_player.play()
            play_pause_btn["text"] = "Pause"

        else:
            vid_player.pause()
            play_pause_btn["text"] = "Play"


    def video_ended(event):
        """ handle video ended """
        progress_slider.set(progress_slider["to"])
        play_pause_btn["text"] = "Play"
        progress_slider.set(0)


    root = tkinter.Tk()
    root.title("Video Player")

    load_btn = tkinter.Button(root, text="Load", command=load_video)
    load_btn.pack()

    vid_player = TkinterVideo(scaled=True, master=root)
    vid_player.pack(expand=True, fill="both")

    play_pause_btn = tkinter.Button(root, text="Play", command=play_pause)
    play_pause_btn.pack()

    skip_plus_5sec = tkinter.Button(root, text="Skip -5 sec", command=lambda: skip(-5))
    skip_plus_5sec.pack(side="left")

    start_time = tkinter.Label(root, text=str(datetime.timedelta(seconds=0)))
    start_time.pack(side="left")

    progress_slider = tkinter.Scale(root, from_=0, to=0, orient="horizontal")
    progress_slider.bind("<ButtonRelease-1>", seek)
    progress_slider.pack(side="left", fill="x", expand=True)

    end_time = tkinter.Label(root, text=str(datetime.timedelta(seconds=0)))
    end_time.pack(side="left")

    vid_player.bind("<<Duration>>", update_duration)
    vid_player.bind("<<SecondChanged>>", update_scale)
    vid_player.bind("<<Ended>>", video_ended )

    skip_plus_5sec = tkinter.Button(root, text="Skip +5 sec", command=lambda: skip(5))
    skip_plus_5sec.pack(side="left")

    root.mainloop()

def browser_page(search_results: dict) -> customtkinter.CTkFrame:
    "The browser page for the front end."
    page = _get_page_template()
    scrollable_frame = _get_scrollable_frame(page)

    #Load videos ascynchronously.
    def load_videos():
        for video in search_results:
            BrowsingVideo(scrollable_frame, video, page)
            if CONST.FRONTEND.current_page != page:
                return
    ActionThread("browsing thread", load_videos, force_new=True)
    return page

def playlist_page(link: str) -> customtkinter.CTkFrame:
    "The playlist page for the frontend."
    page = _get_page_template()

    playlist_videos = []
    download_frame = customtkinter.CTkFrame(page)
    download_options_menu, quality_options_menu, button = _get_download_options(
        download_frame,
        lambda: quality_options_menu.pack(side="left", padx=10, pady=10)
    )

    def batch_download():
        for playlist_video in playlist_videos:
            if playlist_video.is_checked():
                CONST.DOWNLOADER.download(
                    playlist_video.video,
                    download_options_menu.variable.get(),
                    quality_options_menu.variable.get()
                )
    button.command = batch_download
    button.pack(side="left", fill="x")
    download_options_menu.pack(side="left", padx=10, pady=10)
    quality_options_menu.pack(side="left", padx=10, pady=10)
    download_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    scrollable_frame = _get_scrollable_frame(page)
    def load_videos():
        #Get all videos in the playlist.
        while True:
            try: #Try is needed as sometimes the module errors out.
                playlist = YouTube.Playlist(link)
                while playlist.hasMoreVideos:
                    playlist.getNextVideos()
                break
            except KeyError:
                pass
        for video in playlist.videos:
            playlist_videos.append(PlaylistVideo(scrollable_frame, video))

    def errored():
        next_page = "Browser Page"
        CONST.FRONTEND.pages[next_page] = browser_page(
            YouTube.VideosSearch(link, limit = 30).result()["result"]
        )
        CONST.FRONTEND.change_page(next_page)
    ActionThread("playlist loading thread", load_videos, errored, True)

    return page

def video_details_page(
        video_details: dict,
        video: BrowsingVideo = None
    ) -> customtkinter.CTkFrame:
    "The video details page for the front end."

    page = _get_page_template()

    top_bar = customtkinter.CTkFrame(
        page, fg_color=COLOR.get_colour("Dark")
    )
    top_bar.pack(fill="x", side="top", anchor="n", padx=10, ipady=10, pady=10)

    #If there was a video given from the browser page, read it
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
    thumbnail.pack(side="top", anchor="n")

    download_options_menu, quality_options_menu, button = _get_download_options(
        page,
        lambda: quality_options_menu.pack(side="top", anchor="n", padx=10, pady=10)
    )
    button.command = lambda: CONST.DOWNLOADER.download(
        video_details,
        download_options_menu.variable.get(),
        quality_options_menu.variable.get()
    )
    download_options_menu.pack(side="top", anchor="n", pady=(10,0))
    quality_options_menu.pack(side="top",  anchor="n", pady=(10,0))
    button.pack(side="bottom", anchor="s", fill="x", padx=10, ipady=10, pady=(0,10))

    return page

def max_string(string: str, max_char: int):
    "Returns the given string limited to the max character specified"
    return string[:max_char] + ("" if len(string) <= max_char else "...")

def _get_download_options(page, repack_option) -> list[
    customtkinter.CTkOptionMenu,
    customtkinter.CTkOptionMenu,
    customtkinter.CTkButton]:
    "Add an download form options menu, quality options menu and download button to a given page"
    # Download Type Dropdown
    download_option = customtkinter.StringVar()
    download_options_menu = customtkinter.CTkOptionMenu(
        page, variable=download_option,
        values=['Best Video', 'Best Audio', 'mp4', 'mp3'],
        text_color=COLOR.get_colour("Text")
    )
    download_options_menu.set('mp4')

    def on_download_option_changed():
        # Best video/audio doesn't need quality options
        # Hide it when best _ is selected
        match download_option.get():
            case 'Best Video' | 'Best Audio':
                quality_options_menu.pack_forget()
            case _:
                repack_option()
    download_option.trace_variable('w', lambda *e: on_download_option_changed())

    # Quality Dropdown Options
    quality_option = customtkinter.StringVar()
    quality_options_menu = customtkinter.CTkOptionMenu(
        page, variable=quality_option,
        values=['Highest', 'Normal', 'Lowest'],
        text_color=COLOR.get_colour("Text")
    )
    quality_options_menu.set('Highest')

    image = Frontend.get_image("Download.png").subsample(2)
    button = customtkinter.CTkButton(
        page, text="Download", image=image, compound="top",
        width=image.width() + 10, height=image.height(),
        fg_color=COLOR.get_colour("ButtonHover"),
        hover_color=COLOR.get_colour("ButtonHover2"),
        text_color=COLOR.get_colour("Text")
    )

    return download_options_menu, quality_options_menu, button
