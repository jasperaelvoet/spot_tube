import os
from threading import Thread
import time
import tkinter as tk
from sys import platform

import tekore

from classes.save_handler import SaveHandler
from classes.song import Song


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("spot_tube")
        self.canvas = None
        self.color = "Black"
        self.thickness = 1
        self.geometry("600x400")
        self.configure(bg='gray')
        self.iconbitmap('icon.ico')
        self.resizable(False, False)

        self.save_handler = SaveHandler()

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

        if self.save_handler.has_save('id'):
            self.client_id_input.contents.set(self.save_handler.get_save('id'))

        self.text = tk.Text(width=15, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "client secret: ")
        self.text['state'] = 'disabled'
        self.text.grid(row=2, column=0, padx=5, pady=2)

        self.client_secret_input = tk.Entry(width=35)
        self.client_secret_input.grid(row=2, column=1, padx=5, pady=2)
        self.client_secret_input.contents = tk.StringVar()
        self.client_secret_input["textvariable"] = self.client_secret_input.contents

        if self.save_handler.has_save('secret'):
            self.client_secret_input.contents.set(self.save_handler.get_save('secret'))

        self.save_id_value = tk.IntVar()
        self.save_id_checkbox = tk.Checkbutton(text="save client id", bg="gray", activebackground="gray",
                                               variable=self.save_id_value)
        self.save_id_checkbox.grid(row=1, column=2, padx=5, pady=2)

        if self.save_handler.has_save('id'):
            self.save_id_checkbox.select()

        self.save_secret_value = tk.IntVar()
        self.save_secret_checkbox = tk.Checkbutton(text="save client secret", bg="gray", activebackground="gray",
                                                   variable=self.save_secret_value)
        self.save_secret_checkbox.grid(row=2, column=2, padx=5, pady=2)

        if self.save_handler.has_save('secret'):
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

        if self.save_id_value.get() == 1:
            self.save_handler.set_save("id", client_id)
        else:
            self.save_handler.delete_save("id")

        if self.save_secret_value.get() == 1:
            self.save_handler.set_save("secret", client_secret)
        else:
            self.save_handler.delete_save("secret")

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
        self.text.insert("1.0", "path to output folder:")
        self.text['state'] = 'disabled'
        self.text.grid(row=1, column=0, padx=5, pady=2)

        self.path_input = tk.Entry(width=35)
        self.path_input.grid(row=1, column=1, padx=5, pady=2)
        self.path_input.contents = tk.StringVar()
        self.path_input["textvariable"] = self.path_input.contents

        if self.save_handler.has_save('path'):
            self.path_input.contents.set(self.save_handler.get_save('path'))

        self.save_path_value = tk.IntVar()
        self.save_path_checkbox = tk.Checkbutton(text="save path", bg="gray", activebackground="gray",
                                                 variable=self.save_path_value)
        self.save_path_checkbox.grid(row=1, column=2, padx=5, pady=2)

        if self.save_handler.has_save('path'):
            self.save_path_checkbox.select()

        self.test_path_button = \
            tk.Button(text="select", bg="blue", fg="white", activebackground="blue4",
                      activeforeground="white", height=1, width=25, command=self._check_settings)
        self.test_path_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.text = tk.Text(width=15, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "audio quality:")
        self.text['state'] = 'disabled'
        self.text.grid(row=2, column=0, padx=5, pady=2)


        if self.save_handler.has_save('audio_quality'):
            self.audio_quality = tk.StringVar(self, value=self.save_handler.get_save('audio_quality'))
        else:
            self.audio_quality = tk.StringVar(self, value='192')

        options = ['32', '96', '128', '192', '256', '320']

        self.audio_quality_option_menu = tk.OptionMenu(self, self.audio_quality, *options)
        self.audio_quality_option_menu.grid(row=2, column=1)

        self.text = tk.Text(width=25, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "normalize audio level:")
        self.text['state'] = 'disabled'
        self.text.grid(row=3, column=0, padx=5, pady=2)

        self.normalize_audio_level_value = tk.IntVar()
        self.normalize_audio_level_checkbox = tk.Checkbutton(text="(recommended)", bg="gray", activebackground="gray",
                                                             variable=self.normalize_audio_level_value)
        self.normalize_audio_level_checkbox.grid(row=3, column=1, padx=5, pady=2)

        if self.save_handler.has_save('normalize_audio'):
            self.normalize_audio_level_checkbox.select()

    def _check_settings(self):
        self.path_test_text = tk.Label(width=45, height=1, bg='gray', bd=0, fg='gray')
        self.path_test_text.config(text="testing path...")
        self.path_test_text.grid(row=5, column=0, padx=5, pady=10, columnspan=2)

        self.save_handler.set_save('audio_quality', self.audio_quality.get())

        if self.normalize_audio_level_value.get() == 1:
            self.save_handler.set_save('normalize_audio', '')
        else:
            self.save_handler.delete_save('normalize_audio')

        self.out_dir: str = self.path_input.contents.get()

        if self.save_path_value.get() == 1:
            self.save_handler.set_save("path", self.out_dir)
        else:
            self.save_handler.delete_save("path")

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
            with open(self.out_dir + 'test.txt', 'w') as f:
                f.write('testing path')
            os.remove(self.out_dir + 'test.txt')
            self._input_song_links()
        except OSError:
            self.path_test_text.config(text="invalid path", fg='red')

    def _input_song_links(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.text = tk.Text(bg='gray', bd=2, width=60, height=2, borderwidth=0)
        self.text.insert("1.0", "enter your track/album/playlist \nlinks here, separated by enters")
        self.text.grid(row=1, column=0, pady=10, padx=10)

        self.song_links = tk.Text(bg='white', bd=2, width=70, height=16)
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
                track_id = link.replace("https://open.spotify.com/track/", "")
                song_ids.append(track_id)
            if "album" in link:
                album_id = link.replace("https://open.spotify.com/album/", "")
                album = self.spotify.album(album_id)
                for track in album.tracks.items:
                    song_ids.append(track.id)
            if "playlist" in link:
                playlist_id = link.replace("https://open.spotify.com/playlist/", "")
                playlist = self.spotify.playlist(playlist_id)
                for track in playlist.tracks.items:
                    song_ids.append(track.track.id)
        return song_ids

    def _song_download_handler(self):
        self.grid_row_pos = 0
        song_list: list = []

        self.row = {}

        self.song_id_list = self.get_all_song_links(self.links_list)

        time.sleep(1)

        for song_link in self.song_id_list:
            song = Song(song_link, self.out_dir, self.audio_quality.get(),
                        self.spotify, self.normalize_audio_level_value.get())

            text = tk.Label(width=30, height=1, bg='gray', bd=0, fg='black',
                            text=f'{song.album_artist} - {song.track_name}')
            text.grid(row=self.song_id_list.index(song_link) + self.grid_row_pos, column=0, padx=5, pady=10)

            song_status_text = tk.Label(width=50, height=1, bg='gray', bd=0, fg='black',
                                        text=song.status)
            song_status_text.grid(row=self.song_id_list.index(song_link) + self.grid_row_pos,
                                  column=1, padx=5, pady=10)

            song_list.append([song, song_status_text])

            if self.song_id_list.index(song_link) + self.grid_row_pos > 10:
                self.move_grid_up()

            time.sleep(.2)

        for i in range(0, self.grid_row_pos, -1):
            self.move_grid_down()

        grid_move_delay: int = 0
        for song_pair in song_list:
            if grid_move_delay >= 4 and song_list.index(song_pair) + self.grid_row_pos > 8:
                self.move_grid_up()

            Thread(target=song_pair[0].download_song(), daemon=True).start()

            while not song_pair[0].is_installed:
                song_pair[1].config(text=song_pair[0].status)
            time.sleep(0.1)
            song_pair[1].config(text=song_pair[0].status)
            grid_move_delay += 1

