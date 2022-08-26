> # spot_tube
[![release](https://img.shields.io/github/release/jasperaelvoet/spot_tube.svg?style=flat)](https://github.com/jasperaelvoet/spot_tube/releases/latest)
[![downloads](https://img.shields.io/github/downloads/jasperaelvoet/spot_tube/total)](https://github.com/jasperaelvoet/spot_tube/)  
[![start](https://img.shields.io/github/stars/jasperaelvoet/spot_tube?style=social)](https://github.com/jasperaelvoet/spot_tube/stargazers)
# Download songs saved on Spotify via YouTube.
## How the code works:
* 1: Asks user for required info
* 2: Gets song meta-data trough Spotify API
* 3: Uses that meta-data to find the song on YouTube
* 4: Downloads the song if not already installed
* 5: Adds mp3 meta-data and cover art
* 6: Moves song to final directory
## Dependencies:
* ffmpeg (add to path)
* ffmprobe (add to path)
* Spotify api client
## Getting access to the spotify api:
* 1: Go to the <a id="raw-url" href="https://developer.spotify.com/dashboard/">Spotify developer dashboard</a>
* 2: Log in with your Spotify account
* 3: Click on create an app and fill in the app name and description
* 4: On the left, click on show client secret
* 5: Input your client id and secret in the app
## Usage:
#### Release build (recommended) (Windows only):
* 1: Download the latest release <a id="raw-url" href="https://github.com/jasperaelvoet/spot_tube/releases/latest">here</a>
* 2: Extract zip
* 3: Run main.exe
#### From source code:
* 1: <a id="raw-url" href="https://github.com/jasperaelvoet/spot_tube/archive/refs/heads/master.zip">Download source code</a>
* 2: Extract zip
* 3: Install libraries
* 4: Run main.py
## Known issues:
* app might become unresponsive while downloading song
