import sys
import subprocess
import requests
import importlib.metadata
from pathlib import Path
from importlib.util import find_spec
import shutil

def check_internet():
    try:
        requests.head("https://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        return False

if not check_internet():
    print("No internet connection! Please check your internet connection.")
    input("Press Enter to exit...")
    sys.exit()

if shutil.which("ffmpeg") is not None:
    pass
else:
    print("FFmpeg is not installed on your system. Please download it!")
    print("To download FFmpeg: (https://ffmpeg.org/download.html)")
    input("Press Enter to exit...")
    sys.exit()

if find_spec("yt_dlp") is not None:
    pass
else:
    print("yt-dlp is not installed on the python system, please install it!")
    print("")
    print("Windows: pip install yt-dlp")
    print("MacOS: pip install yt-dlp")
    print("Debian/Ubuntu: sudo apt install yt-dlp")
    print("Fedora/RHEL: sudo dnf install yt-dlp")
    print("Arch Linux: sudo pacman -S yt-dlp")
    print("OpenSUSE: sudo zypper install yt-dlp")
    print("")
    input("Press Enter to exit...")
    sys.exit()

def check_ytdlp_version():
        local_version = importlib.metadata.version("yt_dlp")

        response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=5)
        latest_version = response.json()["info"]["version"]

        if local_version == latest_version:
            pass
        else:
            print(f"!!! yt-dlp is not up to date! (Current version: {local_version}) (Latest Version: {latest_version})) !!!")
            print("")
            pass

check_ytdlp_version()

import yt_dlp

print("================")
print("Media Downloader")
print("================")
print("")

def get_valid_url():
    while True:
        url = input("Please enter the YouTube URL: ").strip() 
        if ("youtube" in url or
            "youtu.be" in url or
            "m.youtube" in url or
            "music.youtube" in url):
            return url
        else: 
            print("This YouTube URL is invalid!")

url =  get_valid_url()

while True:
    if "live" in url:
        print("Live broadcasts cannot be downloaded!")
        url = get_valid_url()
    else:
        break

def downloaded_folder():
    while True:
        custom_path = input("Enter the folder to download to (if left blank, the default ‘Downloads’ folder will be used): ").strip()

        if custom_path:
            folder = Path(custom_path)
            if not folder.exists():
                print("Folder not found!")

            else:
                return str(folder)
            
        else:
            return str(Path.home() / "Downloads")
        
download_folder = downloaded_folder()

def check_playlist():
    if "playlist" in url:
        outtmpl = f"{download_folder}/%(playlist_title)s/%(title)s.%(ext)s"
    else:
        outtmpl = f"{download_folder}/%(title)s.%(ext)s"
    return outtmpl

outtmpl = check_playlist()

def video():
    while True:
        print("Select video quality:")
        print("1 - 1080p/2160p (High)")
        print("2 - 720p (Medium)")
        print("3 - 144p/480p (Low)")
        print("If you leave it blank, the highest quality will be selected!")
        choice = input(": ").strip()

        if choice == "1":
            fmt = "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/mp4"
            break
        elif choice == "2":
            fmt = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/mp4"
            break
        elif choice == "3":
            fmt = "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/mp4"
            break
        elif choice == "":
            fmt = "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/mp4"
            break
        else:
            print("Invalid selection!")

    return {
    "format": fmt,
    "postprocessors": [
        {"key": "FFmpegMetadata"},
    ],
    "addmetadata": True,
    "outtmpl": outtmpl,
    "quiet": False,
    }

def audio():
    settings = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
         "key": "FFmpegExtractAudio",
         "preferredcodec": "m4a",
         "preferredquality": "0",
        },

        {"key": "FFmpegMetadata"},
    ],
    "addmetadata": True,
    "outtmpl": outtmpl,
    "quiet": False,
    }
    return settings

def format_choice():
    while True:
        print("Please select the format of the file:")
        print("1 - Video")
        print("2 - Audio")
        print("If you leave it blank, the video format will be selected!")
        choice = input(": ").strip()

        if choice == "1":
           settings = video()
           break
        elif choice == "2":
            settings = audio()
            break
        elif choice == "":
            settings = video()
            break
        else:
            print("Invalid value, please enter 1 or 2!")
    
    with yt_dlp.YoutubeDL(settings) as ydl:
        ydl.download([url])

format_choice()

print("Download Complete!")
input("Press Enter to exit...")
sys.exit()