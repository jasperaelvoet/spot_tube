import os
import time
import threading
from sys import platform
import tkinter as tk
import tekore
from youtubesearchpython import VideosSearch
import yt_dlp
from urllib import request
from eyed3 import id3
from eyed3.id3.frames import ImageFrame
import json


def create_config_file():
    if os.path.exists("config.json"):
        return

    data = {"id": "", "secret": "", "path": ""}

    with open('config.json', 'w') as f:
        json.dump(data, f)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Download Song")
        self.canvas = None
        self.color = "Black"
        self.thickness = 1
        self.geometry("600x400")
        self.configure(bg='gray')
        self.iconbitmap('icon.ico')
        self.resizable(False, False)
        create_config_file()
        self._create_spotify_api_widgets()

    def _create_spotify_api_widgets(self):
        self.text = tk.Text(width=25, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "connect to spotify API")
        self.text['state'] = 'disabled'
        self.text.grid(row=0, column=0, columnspan=2, pady=10)

        self.text = tk.Text(width=15, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "client id: ")
        self.text['state'] = 'disabled'
        self.text.grid(row=1, column=0, padx=5, pady=2)

        self.client_id_input = tk.Entry(width=35)
        self.client_id_input.grid(row=1, column=1, padx=5, pady=2)
        self.client_id_input.contents = tk.StringVar()
        self.client_id_input["textvariable"] = self.client_id_input.contents
        with open('config.json', 'r') as f:
            self.client_id_input.contents.set(json.load(f)['id'])

        self.text = tk.Text(width=15, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "client secret: ")
        self.text['state'] = 'disabled'
        self.text.grid(row=2, column=0, padx=5, pady=2)

        self.client_secret_input = tk.Entry(width=35)
        self.client_secret_input.grid(row=2, column=1, padx=5, pady=2)
        self.client_secret_input.contents = tk.StringVar()
        self.client_secret_input["textvariable"] = self.client_secret_input.contents
        with open('config.json', 'r') as f:
            self.client_secret_input.contents.set(json.load(f)['secret'])

        self.save_id_value = tk.IntVar()
        self.save_id_checkbox = tk.Checkbutton(text="save client id", bg="gray", activebackground="gray",
                                               variable=self.save_id_value)
        self.save_id_checkbox.grid(row=1, column=2, padx=5, pady=2)
        with open('config.json', 'r') as f:
            if not json.load(f)['id'] == "":
                self.save_id_checkbox.select()

        self.save_secret_value = tk.IntVar()
        self.save_secret_checkbox = tk.Checkbutton(text="save client secret", bg="gray", activebackground="gray",
                                                   variable=self.save_secret_value)
        self.save_secret_checkbox.grid(row=2, column=2, padx=5, pady=2)
        with open('config.json', 'r') as f:
            if not json.load(f)['secret'] == "":
                self.save_secret_checkbox.select()

        self.connect_to_spotify_api_button = \
            tk.Button(text="connect", bg="blue", fg="white", activebackground="blue4",
                      activeforeground="white", height=1, width=25, command=self._connect_to_spotify_api)
        self.connect_to_spotify_api_button.grid(row=3, column=0, columnspan=2, pady=10)

    def _connect_to_spotify_api(self):
        self.connection_status_text = tk.Label(width=45, height=1, bg='gray', bd=0, fg='gray')
        self.connection_status_text.config(text="connecting...")
        self.connection_status_text.grid(row=4, column=0, padx=5, pady=10, columnspan=2)

        client_id: str = self.client_id_input.contents.get()
        client_secret: str = self.client_secret_input.contents.get()

        with open('config.json', 'r') as f:
            data = json.load(f)

        if self.save_id_value.get() == 1:
            data["id"] = client_id
        else:
            data["id"] = ""

        if self.save_secret_value.get() == 1:
            data["secret"] = client_secret
        else:
            data["secret"] = ""

        with open('config.json', 'w') as f:
            json.dump(data, f)

        try:
            app_token = tekore.request_client_token(client_id, client_secret)
            self.spotify = tekore.Spotify(app_token)
            self._set_path()
        except tekore.BadRequest:
            self.connection_status_text.config(text="failed to connect, check your client id and secret", fg='red')

    def _set_path(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.text = tk.Text(width=25, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "set up paths")
        self.text['state'] = 'disabled'
        self.text.grid(row=0, column=0, columnspan=2, pady=10)

        self.text = tk.Text(width=15, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "path to output folder")
        self.text['state'] = 'disabled'
        self.text.grid(row=1, column=0, padx=5, pady=2)

        self.path_input = tk.Entry(width=35)
        self.path_input.grid(row=1, column=1, padx=5, pady=2)
        self.path_input.contents = tk.StringVar()
        self.path_input["textvariable"] = self.path_input.contents

        with open('config.json', 'r') as f:
            self.path_input.contents.set(json.load(f)['path'])

        self.save_path_value = tk.IntVar()
        self.save_path_checkbox = tk.Checkbutton(text="save path", bg="gray", activebackground="gray",
                                                 variable=self.save_path_value)
        self.save_path_checkbox.grid(row=1, column=2, padx=5, pady=2)
        with open('config.json', 'r') as f:
            if not json.load(f)['path'] == "":
                self.save_path_checkbox.select()

        self.test_path_button = \
            tk.Button(text="select", bg="blue", fg="white", activebackground="blue4",
                      activeforeground="white", height=1, width=25, command=self._check_settings)
        self.test_path_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.text = tk.Text(width=15, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "audio quality")
        self.text['state'] = 'disabled'
        self.text.grid(row=2, column=0, padx=5, pady=2)

        self.audio_quality = tk.StringVar(self, value='256')

        options = ['32', '96', '128', '192', '256', '320']

        self.audio_quality_option_menu = tk.OptionMenu(self, self.audio_quality, *options)
        self.audio_quality_option_menu .grid(row=2, column=1)

    def _check_settings(self):
        self.path_test_text = tk.Label(width=45, height=1, bg='gray', bd=0, fg='gray')
        self.path_test_text.config(text="testing path...")
        self.path_test_text.grid(row=4, column=0, padx=5, pady=10, columnspan=2)

        self.out_dir: str = self.path_input.contents.get()

        with open('config.json', 'r') as f:
            data = json.load(f)
        if self.save_path_value.get() == 1:
            data["path"] = self.out_dir
        else:
            data["path"] = ""

        with open('config.json', 'w') as f:
            json.dump(data, f)

        if not self.out_dir[-1] == ("\\" or "/"):
            if platform == "win32":
                self.out_dir += "\\"
            else:
                self.out_dir += "/"

        try:
            with open(self.out_dir + 'test.txt', 'w') as f:
                f.write('testing path')
            os.remove(self.out_dir + 'test.txt')
            self._input_song_links()
        except OSError:
            self.path_test_text.config(text="invalid path", fg='red')

    def _input_song_links(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.text = tk.Text(bg='gray', bd=2, width=60, height=1, borderwidth=0)
        self.text.insert("1.0", "enter your song links here, separated by enters")
        self.text.grid(row=1, column=0, pady=10, padx=10)

        self.song_links = tk.Text(bg='white', bd=2, width=70, height=18)
        self.song_links.grid(row=2, column=0, pady=10, padx=10)

        self.download_songs_button = \
            tk.Button(text="download songs", bg="blue", fg="white", activebackground="blue4",
                      activeforeground="white", height=1, width=25, command=self._get_songs)
        self.download_songs_button.grid(row=3, column=0, columnspan=2, pady=10)

    def move_grid_up(self):
        self.grid_row_pos -= 1
        widget_id: int = 0

        for widget in self.winfo_children():
            if widget_id in self.row.keys():
                self.row[widget_id] = self.row.get(widget_id) - 1
            else:
                self.row[widget_id] = widget.grid_info()["row"] - 1
            if self.row[widget_id] < 0:
                widget.grid_remove()
            else:
                widget.grid(row=self.row[widget_id])
            widget_id += 1

    def move_grid_down(self):
        self.grid_row_pos += 1
        widget_id: int = 0

        for widget in self.winfo_children():
            if widget_id in self.row.keys():
                self.row[widget_id] = self.row.get(widget_id) + 1
            else:
                self.row[widget_id] = widget.grid_info()["row"] + 1
            if self.row[widget_id] < 0:
                widget.grid_remove()
            else:
                widget.grid(row=self.row[widget_id])
            widget_id += 1

    def _get_songs(self):
        self.song_links_list = self.song_links.get("1.0", "end-1c").splitlines()

        for widgets in reversed(self.winfo_children()):
            widgets.destroy()

        threading.Thread(target=self._song_download_handler, daemon=True).start()

    def _song_download_handler(self):
        self.grid_row_pos = 0
        song_list: list = []

        self.row = {}

        for song_link in self.song_links_list:
            song = Song(song_link)

            text = tk.Label(width=30, height=1, bg='gray', bd=0, fg='black',
                            text=f'{song.track_artist} - {song.track_name}')
            text.grid(row=self.song_links_list.index(song_link) + self.grid_row_pos, column=0, padx=5, pady=10)

            song_status_text = tk.Label(width=50, height=1, bg='gray', bd=0, fg='black',
                                        text=song.status)
            song_status_text.grid(row=self.song_links_list.index(song_link) + self.grid_row_pos,
                                  column=1, padx=5, pady=10)

            song_list.append([song, song_status_text])

            if self.song_links_list.index(song_link) + self.grid_row_pos > 10:
                self.move_grid_up()

        for i in range(0, self.grid_row_pos, -1):
            self.move_grid_down()

        grid_move_delay: int = 0
        for song_pair in song_list:
            if grid_move_delay >= 4 and song_list.index(song_pair) + self.grid_row_pos > 8:
                self.move_grid_up()

            threading.Thread(target=song_pair[0].download_song).start()

            while not song_pair[0].is_installed:
                song_pair[1].config(text=song_pair[0].status)

            grid_move_delay += 1


class Song:
    def __init__(self, song_link):
        try:
            song_link = song_link.replace("https://open.spotify.com/track/", "")
            song_track = app.spotify.track(song_link)

            self.track_artist = song_track.artists[0].name
            self.album_name = song_track.album.name
            self.track_name = song_track.name
            self.album_artist = song_track.album.artists[0].name
            self.artist_url = song_track.artists[0].external_urls.get("spotify")
            self.release_date = song_track.album.release_date
            self.cover_art_url = song_track.album.images[0].url
            self.disc_num = song_track.disc_number
            self.track_num = song_track.track_number
            self.status = "waiting for download"
            self.is_usable = True
            self.is_installed = False

        except tekore.BadRequest:
            self.status = "invalid id"
            self.track_artist = "n/a"
            self.track_name = "n/a"
            self.is_usable = False

    def download_song(self):
        self.status = "checking if already installed"
        out_name = f'{self.track_artist} - {self.track_name}'
        out_name = out_name.replace("/", "")
        out_name = out_name.replace("\\", "")

        if not self.is_usable:
            time.sleep(0.1)
            self.is_installed = True
            return

        if os.path.exists(app.out_dir + out_name + r".mp3"):
            self.status = "already installed"
            time.sleep(0.1)
            self.is_installed = True
            return

        try:
            self.status = "searching on youtube"
            video_search = VideosSearch(f'{out_name} (audio)', limit=1)
            video_link = video_search.result()['result'][0]['link']
        except:
            self.status = "failed to search song"
            time.sleep(0.1)
            self.is_installed = True
            return

        try:
            self.status = "downloading"
            ydl_opts = {
                'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3', 'preferredquality': app.audio_quality.get()}],
                'outtmpl': 'temp_song',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
        except:
            self.status = "failed to download song"
            time.sleep(0.1)
            self.is_installed = True
            return

        try:
            self.status = "adding id3 tags"
            song = "temp_song.mp3"
            tag = id3.Tag()
            tag.parse(song)
            tag.artist = self.track_artist
            tag.album = self.album_name
            tag.title = self.track_name
            tag.album_artist = self.album_artist
            tag.artist_url = self.artist_url
            tag.release_date = self.release_date
            tag.disc_num = self.disc_num
            tag.track_num = self.track_num

            self.status = "adding cover image"
            request.urlretrieve(self.cover_art_url, "cover.jpg")
            tag.images.set(ImageFrame.FRONT_COVER, open('cover.jpg', 'rb').read(), 'image/jpeg')
            os.remove("cover.jpg")

            tag.save()
        except:
            self.status = "failed to add id3 tags"
            time.sleep(0.1)
            self.is_installed = True
            return

        try:
            self.status = "moving song to final folder"
            os.rename("temp_song.mp3", app.out_dir + out_name + r".mp3")
        except:
            self.status = "failed to move song to final directory"
            time.sleep(0.1)
            self.is_installed = True
            return

        self.status = "installed"
        time.sleep(0.1)
        self.is_installed = True
        return


app = App()
app.mainloop()
