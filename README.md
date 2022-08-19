> # spot_tube
[![GitHub release](https://img.shields.io/github/release/jasperaelvoet/spot_tube.svg?style=flat)](https://github.com/jasperaelvoet/spot_tube/releases)
# Download spotify songs trough YouTube.
#### how the code works:
* 1: asks user for required info
* 2: gets song meta-data trough Spotify API
* 3: uses that meta-data to find the song on YouTube
* 4: downloads the song if not already installed
* 5: adds mp3 meta-data and cover art
* 6: moves song to final directory
#### dependencies:
* ffmpeg (add to path)
* ffmprobe (add to path)
## usage:
#### release build (recommended):
* 1: download the latest release <a id="raw-url" href="https://github.com/jasperaelvoet/spot_tube/releases">here</a>
* 2: extract zip
* 3: run main.exe
#### from source code:
* 1: <a id="raw-url" href="https://github.com/jasperaelvoet/spot_tube/archive/refs/heads/master.zip">Download source code</a>
* 2: extract zip
* 3: install libraries
* 4: run main.py