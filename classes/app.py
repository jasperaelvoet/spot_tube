import os
import time
from threading import Thread
import tkinter as tk

from sys import platform

from classes.save_handler import SaveHandler
from classes.song import Song
import classes.spotify as spotify


def read_rgb(rgb):
    return "#%02x%02x%02x" % rgb


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("spot_tube")
        self.canvas = None
        self.color = "Black"
        self.thickness = 1
        self.geometry("550x200")
        self.configure(bg=read_rgb((64, 64, 64)))
        self.iconbitmap('icon.ico')
        self.resizable(False, False)

        self.save_handler = SaveHandler()

        self._create_spotify_api_widgets()

    def _create_spotify_api_widgets(self):

        text = tk.Label(height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((255, 255, 255)), bd=0,
                        font=("Arial", 25, 'bold'), text="connect to spotify API")
        text.grid(row=0, column=0, columnspan=3, pady=10)

        text = tk.Label(width=15, height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((192, 192, 192)), bd=0,
                        font=("Arial", 12, 'bold'), text="client id: ")
        text.grid(row=1, column=0, padx=5, pady=2)

        self.client_id_value = tk.StringVar()
        self.client_id_input = tk.Entry(width=35, textvariable=self.client_id_value, bg=read_rgb((84, 84, 84)),
                                        bd=0, font=("Arial", 8, 'bold'), fg=read_rgb((0, 0, 0)))
        self.client_id_input.grid(row=1, column=1, padx=5, pady=2)

        if self.save_handler.has_save('id'):
            self.client_id_value.set(self.save_handler.get_save('id'))

        text = tk.Label(width=15, height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((192, 192, 192)), bd=0,
                        font=("Arial", 12, 'bold'), text="client secret: ")
        text.grid(row=2, column=0, padx=5, pady=2)

        self.client_secret_value = tk.StringVar()
        self.client_secret_input = tk.Entry(width=35, textvariable=self.client_secret_value, bg=read_rgb((84, 84, 84)),
                                            bd=0, font=("Arial", 8, 'bold'), fg=read_rgb((0, 0, 0)))
        self.client_secret_input.grid(row=2, column=1, padx=5, pady=2)

        if self.save_handler.has_save('secret'):
            self.client_secret_value.set(self.save_handler.get_save('secret'))

        self.save_id_value = tk.IntVar()
        self.save_id_checkbox = tk.Checkbutton(text="save client id", activebackground=read_rgb((64, 64, 64)),
                                               variable=self.save_id_value, bg=read_rgb((64, 64, 64)),
                                               font=("Arial", 8, 'bold'), fg=read_rgb((192, 192, 192)),
                                               selectcolor=read_rgb((64, 64, 64)))
        self.save_id_checkbox.grid(row=1, column=2, padx=5, pady=2)

        if self.save_handler.has_save('id'):
            self.save_id_checkbox.select()

        self.save_secret_value = tk.IntVar()
        self.save_secret_checkbox = tk.Checkbutton(text="save client secret", activebackground=read_rgb((64, 64, 64)),
                                                   variable=self.save_secret_value, bg=read_rgb((64, 64, 64)),
                                                   font=("Arial", 8, 'bold'), fg=read_rgb((192, 192, 192)),
                                                   selectcolor=read_rgb((64, 64, 64)))
        self.save_secret_checkbox.grid(row=2, column=2, padx=5, pady=2)

        if self.save_handler.has_save('secret'):
            self.save_secret_checkbox.select()

        button = \
            tk.Button(text="connect", height=2, width=60, command=self._connect_to_spotify_api, bd=0,
                      bg=read_rgb((84, 84, 84)), font=("Arial", 8, 'bold'), activebackground=read_rgb((64, 64, 64)))
        button.grid(row=3, column=0, columnspan=3, pady=10)

    def _connect_to_spotify_api(self):
        self.connection_status_text = tk.Label(width=45, height=1, bg=read_rgb((64, 64, 64)), bd=0, fg='gray',
                                               font=("Arial", 8, 'bold'), text="connecting...")
        self.connection_status_text.grid(row=4, column=0, padx=5, pady=10, columnspan=3)

        client_id: str = self.client_id_value.get()
        client_secret: str = self.client_secret_value.get()

        try:
            self.access_token = spotify.get_access_token(client_id, client_secret)

            if self.save_id_value.get() == 1:
                self.save_handler.set_save("id", client_id)
            else:
                self.save_handler.delete_save("id")

            if self.save_secret_value.get() == 1:
                self.save_handler.set_save("secret", client_secret)
            else:
                self.save_handler.delete_save("secret")

            self._set_path()
        except KeyError:
            self.connection_status_text.config(text="failed to connect, check your client id and secret", fg='red')

    def _set_path(self):
        self.geometry("550x230")

        for widgets in self.winfo_children():
            widgets.destroy()

        text = tk.Label(height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((255, 255, 255)), bd=0,
                        font=("Arial", 25, 'bold'), text="configure download")
        text.grid(row=0, column=0, columnspan=3, pady=10)

        text = tk.Label(width=15, height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((192, 192, 192)), bd=0,
                        font=("Arial", 12, 'bold'), text="output folder: ")
        text.grid(row=1, column=0, padx=5, pady=2)

        self.path_value = tk.StringVar()
        self.path_input = tk.Entry(width=45, textvariable=self.path_value, bg=read_rgb((84, 84, 84)),
                                   bd=0, font=("Arial", 8, 'bold'), fg=read_rgb((0, 0, 0)))
        self.path_input.grid(row=1, column=1, padx=5, pady=2)

        if self.save_handler.has_save('path'):
            self.path_value.set(self.save_handler.get_save('path'))

        self.save_path_value = tk.IntVar()
        self.save_path_checkbox = tk.Checkbutton(text="save path", activebackground=read_rgb((64, 64, 64)),
                                                 variable=self.save_path_value, bg=read_rgb((64, 64, 64)),
                                                 font=("Arial", 8, 'bold'), fg=read_rgb((192, 192, 192)),
                                                 selectcolor=read_rgb((64, 64, 64)))
        self.save_path_checkbox.grid(row=1, column=2, padx=5, pady=2)

        if self.save_handler.has_save('path'):
            self.save_path_checkbox.select()

        button = \
            tk.Button(text="continue", height=2, width=60, command=self._check_settings, bd=0,
                      bg=read_rgb((84, 84, 84)), font=("Arial", 8, 'bold'), activebackground=read_rgb((64, 64, 64)))
        button.grid(row=4, column=0, columnspan=3, pady=10)

        text = tk.Label(width=15, height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((192, 192, 192)), bd=0,
                        font=("Arial", 12, 'bold'), text="audio quality: ")
        text.grid(row=2, column=0, padx=5, pady=2)

        if self.save_handler.has_save('audio_quality'):
            self.audio_quality = tk.StringVar(self, value=self.save_handler.get_save('audio_quality'))
        else:
            self.audio_quality = tk.StringVar(self, value='192')

        options = ['32', '96', '128', '192', '256', '320']

        self.audio_quality_option_menu = tk.OptionMenu(self, self.audio_quality, *options)
        self.audio_quality_option_menu.grid(row=2, column=1)

        text = tk.Label(width=15, height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((192, 192, 192)), bd=0,
                        font=("Arial", 12, 'bold'), text="normalize audio: ")
        text.grid(row=3, column=0, padx=5, pady=2)

        self.normalize_audio_level_value = tk.IntVar()
        self.normalize_audio_level_checkbox = \
            tk.Checkbutton(text="(recommended)", activebackground=read_rgb((64, 64, 64)),
                           variable=self.normalize_audio_level_value, bg=read_rgb((64, 64, 64)),
                           font=("Arial", 8, 'bold'), fg=read_rgb((192, 192, 192)), selectcolor=read_rgb((64, 64, 64)))
        self.normalize_audio_level_checkbox.grid(row=3, column=1, padx=5, pady=2)

        if self.save_handler.has_save('normalize_audio'):
            self.normalize_audio_level_checkbox.select()

    def _check_settings(self):
        self.path_test_text = tk.Label(width=45, height=1, bg=read_rgb((64, 64, 64)), bd=0, fg='gray',
                                       font=("Arial", 8, 'bold'), text="testing path...")
        self.path_test_text.grid(row=5, column=0, padx=5, pady=10, columnspan=3)

        self.save_handler.set_save('audio_quality', self.audio_quality.get())

        if self.normalize_audio_level_value.get() == 1:
            self.save_handler.set_save('normalize_audio', '')
        else:
            self.save_handler.delete_save('normalize_audio')

        self.out_dir: str = self.path_value.get()

        try:
            if not self.out_dir[-1] == ("\\" or "/"):
                if platform == "win32":
                    self.out_dir += "\\"
                else:
                    self.out_dir += "/"
        except IndexError:
            self.path_test_text.config(text="no path input", fg='red')
            return

        try:
            if not os.path.exists(self.out_dir):
                raise OSError

            if self.save_path_value.get() == 1:
                self.save_handler.set_save("path", self.out_dir)
            else:
                self.save_handler.delete_save("path")

            self._input_song_links()
        except OSError:
            self.path_test_text.config(text="invalid path OR path does not exist", fg='red')

    def _input_song_links(self):
        self.geometry("550x300")

        for widgets in self.winfo_children():
            widgets.destroy()

        text = tk.Label(height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((255, 255, 255)), bd=0,
                        font=("Arial", 12, 'bold'), width=55,
                        text="enter your track/album/playlist/artist links here, separated by enters")
        text.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

        self.song_links = tk.Text(bd=0, height=12, width=80, bg=read_rgb((84, 84, 84)),
                                  font=("Arial", 8, 'bold'), fg=read_rgb((0, 0, 0)))
        self.song_links.grid(row=2, column=0, columnspan=3, pady=10, padx=10)

        button = \
            tk.Button(text="download songs", height=2, width=60, command=self._get_songs, bd=0,
                      bg=read_rgb((84, 84, 84)), font=("Arial", 8, 'bold'), activebackground=read_rgb((64, 64, 64)))
        button.grid(row=3, column=0, columnspan=3, pady=10)

    def move_grid_up(self):
        self.grid_row_pos -= 1
        widget_id: int = 0

        for widget in self.winfo_children():
            if widget_id in self.row.keys():
                self.row[widget_id] = self.row.get(widget_id) - 1
            else:
                self.row[widget_id] = widget.grid_info()["row"] - 1
            row = self.row[widget_id]
            if row < 0:
                widget.grid_remove()
            elif row > 15:
                widget.grid_remove()
            else:
                widget.grid(row=row)
            widget_id += 1

    def move_grid_down(self):
        self.grid_row_pos += 1
        widget_id: int = 0

        for widget in self.winfo_children():
            if widget_id in self.row.keys():
                self.row[widget_id] = self.row.get(widget_id) + 1
            else:
                self.row[widget_id] = widget.grid_info()["row"] + 1
            row = self.row[widget_id]
            if row < 0:
                widget.grid_remove()
            elif row > 15:
                widget.grid_remove()
            else:
                widget.grid(row=row)
            widget_id += 1

    def _get_songs(self):
        self.links_list = self.song_links.get("1.0", "end-1c").splitlines()

        for widgets in reversed(self.winfo_children()):
            widgets.destroy()

        Thread(target=self._song_download_handler, daemon=True).start()

    def get_all_song_links(self, links):
        song_ids = []
        for link in links:
            if "track" in link:
                track_id = link.replace("https://open.spotify.com/track/", "").split("?")[0]
                song_ids.append(track_id)
            if "album" in link:
                album_id = link.replace("https://open.spotify.com/album/", "").split("?")[0]
                album = spotify.get_album(self.access_token, album_id)
                for i in album['tracks']['items']:
                    song_ids.append(i['id'])
            if "playlist" in link:
                playlist_id = link.replace("https://open.spotify.com/playlist/", "").split("?")[0]
                playlist = spotify.get_playlist(self.access_token, playlist_id)
                for i in playlist['tracks']['items']:
                    song_ids.append(i['id'])
            if "artist" in link:
                artist_id = link.replace("https://open.spotify.com/artist/", "").split("?")[0]
                artist = spotify.get_artist_albums(self.access_token, artist_id)
                for a in artist['items']:
                    album_id = a['uri'].replace('spotify:album:', "")
                    album = spotify.get_album(self.access_token, album_id)
                    for s in album['tracks']['items']:
                        song_ids.append(s['id'])
        return song_ids

    def _add_song_to_display(self, song_link):
        song = Song(song_link, self.out_dir, self.audio_quality.get(),
                    self.access_token, self.normalize_audio_level_value.get())

        list_index = self.song_id_list.index(song_link)


        row_pos: int = list_index + self.grid_row_pos

        text = tk.Label(width=50, height=1, bg=read_rgb((64, 64, 64)), bd=0, fg=read_rgb((192, 192, 192)),
                        text=f'{song.album_artist} - {song.track_name}', font=("Arial", 8, 'bold'))
        text.grid(row=row_pos, column=0,
                  columnspan=2, padx=5, pady=10)

        song_status_text = tk.Label(width=20, height=1, bg=read_rgb((64, 64, 64)), bd=0,
                                    fg=read_rgb((192, 192, 192)), text=song.status, font=("Arial", 8, 'bold'))
        song_status_text.grid(row=row_pos, column=2, padx=5, pady=10)

        self.song_list.append([song, song_status_text])

    def _handle_updatable_download(self, song_pair):
        Thread(target=song_pair[0].download_song).start()

        song_pair[1].config(fg=read_rgb((0, 0, 255)))

        while not (song_pair[0].successfully_installed or song_pair[0].failed_install):
            song_pair[1].config(text=song_pair[0].status)

        song_pair[1].config(text=song_pair[0].status)
        if song_pair[0].failed_install:
            song_pair[1].config(fg=read_rgb((255, 0, 0)))
            self.downloads_failed += 1
        elif song_pair[0].successfully_installed:
            song_pair[1].config(fg=read_rgb((0, 255, 0)))
            self.downloads_successful += 1

    def _song_download_handler(self):
        self.grid_row_pos = 0
        self.song_list: list = []

        self.row = {}

        self.song_id_list = self.get_all_song_links(self.links_list)

        grid_move_delay: int = 0

        self.downloads_successful = 0
        self.downloads_failed = 0

        current_downloading_song: int = 0

        # load first 10 songs
        for song_link in self.song_id_list[:10]:
            self._add_song_to_display(song_link)

        # download all songs if less than 10
        if len(self.song_id_list) < 10:
            for _ in range(len(self.song_id_list)):
                song_pair = self.song_list[current_downloading_song]
                if grid_move_delay >= 6:
                    self.move_grid_up()
                self._handle_updatable_download(song_pair)
                current_downloading_song += 1
                grid_move_delay += 1
            return self._summary()
        else:
            # download songs and load new one until 10 left
            for song_link in self.song_id_list[10:]:
                self._add_song_to_display(song_link)
                song_pair = self.song_list[current_downloading_song]
                if grid_move_delay >= 6:
                    self.move_grid_up()
                self._handle_updatable_download(song_pair)
                current_downloading_song += 1
                grid_move_delay += 1
            # download last 10 songs that have already been loaded
            for _ in range(10):
                song_pair = self.song_list[current_downloading_song]
                if grid_move_delay >= 6:
                    self.move_grid_up()
                self._handle_updatable_download(song_pair)
                current_downloading_song += 1
                grid_move_delay += 1
            return self._summary()

    def _summary(self):
        self.geometry("550x200")

        for widgets in self.winfo_children():
            widgets.destroy()

        text = tk.Label(height=1, width=55, bg=read_rgb((64, 64, 64)), fg=read_rgb((255, 255, 255)), bd=0,
                        font=("Arial", 12, 'bold'), text="downloads completed")
        text.grid(row=0, column=0, columnspan=3, pady=10)

        text = tk.Label(height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((0, 255, 0)), bd=0,
                        font=("Arial", 12, 'bold'), width=15,
                        text=f"Successful: {self.downloads_successful}")
        text.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

        text = tk.Label(height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((255, 0, 0)), bd=0,
                        font=("Arial", 12, 'bold'), width=15,
                        text=f"Failed: {self.downloads_failed}")
        text.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

        text = tk.Label(height=1, bg=read_rgb((64, 64, 64)), fg=read_rgb((0, 0, 255)), bd=0,
                        font=("Arial", 12, 'bold'), width=15,
                        text=f"Total: {self.downloads_failed + self.downloads_successful}")
        text.grid(row=3, column=0, columnspan=3, padx=5, pady=10)