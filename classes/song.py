import os
import time
from urllib import request

import tekore
import yt_dlp
from eyed3 import id3
from eyed3.id3.frames import ImageFrame
from pydub import AudioSegment
from youtubesearchpython import VideosSearch


class Song:
    def __init__(self, song_link, out_dir, audio_quality, spotify, do_audio_normalization):
        self.spotify = spotify
        self.audio_quality = audio_quality
        self.out_dir = out_dir
        self.do_audio_normalization = do_audio_normalization

        try:
            song_track = self.spotify.track(song_link)

            self.track_artist = song_track.artists[0].name
            for artists in song_track.artists[1:]:
                self.track_artist += " & " + artists.name

            self.album_name = song_track.album.name
            self.track_name = song_track.name
            self.album_artist = song_track.album.artists[0].name
            self.artist_url = song_track.artists[0].external_urls.get("spotify")
            self.release_date = song_track.album.release_date
            self.cover_art_url = song_track.album.images[0].url
            self.disc_num = song_track.disc_number
            self.track_num = song_track.track_number

            try:
                self.genre = self.spotify.artist(song_track.album.artists[0].id).genres[0]
                for genre in self.spotify.artist(song_track.album.artists[0].id).genres[1:]:
                    self.genre += " & " + genre
            except Exception as e:
                print(e)
                self.genre = "n/a"

            self.status = "waiting for download"
            self.is_usable = True
            self.successfully_installed = False
            self.failed_install = False

        except tekore.BadRequest:
            self.status = "invalid id"
            self.album_artist = "n/a"
            self.track_name = "n/a"
            self.is_usable = False
            self.failed_install = True

    @staticmethod
    def match_target_amplitude(sound, target_dBFS):
        change_in_dBFS = target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def normalize_audio_level(self):
        sound = AudioSegment.from_file("temp_song.mp3", "mp3")
        normalized_sound = self.match_target_amplitude(sound, -20.0)
        normalized_sound.export("temp_song.mp3", format="mp3", bitrate=self.audio_quality + 'k')

    def download_song(self):
        self.status = "checking if already installed"
        out_name = f'{self.album_artist} - {self.track_name}'
        out_name = out_name.replace("/", "")
        out_name = out_name.replace("\\", "")
        out_name = out_name.replace('"', "")
        out_name = out_name.replace("'", "")

        if not self.is_usable:
            time.sleep(0.1)
            self.failed_install = True
            return

        if os.path.exists(self.out_dir + out_name + r".mp3"):
            self.status = "already installed"
            time.sleep(0.1)
            self.successfully_installed = True
            return

        try:
            self.status = "searching on youtube"
            video_search = VideosSearch(f'{out_name} (audio)', limit=1)
            video_link = video_search.result()['result'][0]['link']
        except Exception as e:
            print(e)
            self.status = "failed to search song"
            time.sleep(0.1)
            self.failed_install = True
            return

        try:
            self.status = "downloading"
            ydl_opts = {
                'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3', 'preferredquality': self.audio_quality}],
                'outtmpl': 'temp_song',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
        except Exception as e:
            print(e)
            self.status = "failed to download song"
            time.sleep(0.1)
            self.failed_install = True
            return

        if self.do_audio_normalization == 1:
            try:
                self.status = "normalizing audio level"
                time.sleep(0.1)
                self.normalize_audio_level()
            except Exception as e:
                print(e)
                self.status = "failed to normalize audio level"
                time.sleep(0.1)
                self.failed_install = True
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
            tag.genre = self.genre

            self.status = "adding cover image"
            request.urlretrieve(self.cover_art_url, "cover.jpg")
            tag.images.set(ImageFrame.FRONT_COVER, open('cover.jpg', 'rb').read(), 'image/jpeg')
            os.remove("cover.jpg")

            tag.save()
        except Exception as e:
            print(e)
            self.status = "failed to add id3 tags"
            time.sleep(0.1)
            self.failed_install = True
            return

        try:
            self.status = "moving song to final folder"
            os.rename("temp_song.mp3", self.out_dir + out_name + r".mp3")
        except Exception as e:
            print(e)
            self.status = "failed to move song to final directory"
            time.sleep(0.1)
            self.failed_install = True
            return

        self.status = "installed"
        time.sleep(0.1)
        self.successfully_installed = True
        return
