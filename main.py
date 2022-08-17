import tkinter as tk
import tekore
import os
from sys import platform

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
        self._input_song_links()
        # self._create_spotify_api_widgets()

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

        self.text = tk.Text(width=15, height=1, bg='gray', bd=0)
        self.text.insert("1.0", "client secret: ")
        self.text['state'] = 'disabled'
        self.text.grid(row=2, column=0, padx=5, pady=2)

        self.client_secret_input = tk.Entry(width=35)
        self.client_secret_input.grid(row=2, column=1, padx=5, pady=2)
        self.client_secret_input.contents = tk.StringVar()
        self.client_secret_input["textvariable"] = self.client_secret_input.contents

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

        try:
            tekore.request_client_token(client_id, client_secret)
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

        self.test_path_button = \
            tk.Button(text="connect", bg="blue", fg="white", activebackground="blue4",
                      activeforeground="white", height=1, width=25, command=self._test_path)
        self.test_path_button.grid(row=3, column=0, columnspan=2, pady=10)

    def _test_path(self):
        self.path_test_text = tk.Label(width=45, height=1, bg='gray', bd=0, fg='gray')
        self.path_test_text.config(text="testing path...")
        self.path_test_text.grid(row=4, column=0, padx=5, pady=10, columnspan=2)

        out_dir: str = self.path_input.contents.get()

        if not out_dir[-1] == ("\\" or "/"):
            if platform == "win32":
                out_dir += "\\"
            else:
                out_dir += "/"

        try:
            with open(out_dir+'test.txt', 'w') as f:
                f.write('testing path')
            os.remove(out_dir+'test.txt')
            self._input_song_links()
        except OSError:
            self.path_test_text.config(text="invalid path", fg='red')

    def _input_song_links(self):
        for widgets in self.winfo_children():
            widgets.destroy()

        self.text = tk.Text(bg='gray', bd=2, width=60, height=1, borderwidth=0)
        self.text.insert("1.0", "enter your song links here, separated by a space or enter")
        self.text.grid(row=1, column=0, pady=10, padx=10)

        self.song_links = tk.Text(bg='white', bd=2, width=70, height=18)
        self.song_links.grid(row=2, column=0, pady=10, padx=10)

        self.download_songs_button = \
            tk.Button(text="download songs", bg="blue", fg="white", activebackground="blue4",
                      activeforeground="white", height=1, width=25, command=self._download_song_links)
        self.download_songs_button.grid(row=3, column=0, columnspan=2, pady=10)

    def _download_song_links(self):
        print(self.song_links.get("1.0", "end-1c"))


myapp = App()
myapp.mainloop()
