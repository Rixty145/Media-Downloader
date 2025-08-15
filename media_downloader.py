import sys
import subprocess
import requests
import importlib.metadata
from pathlib import Path
from importlib.util import find_spec
import shutil
import yt_dlp

def check_internet():
    try:
        requests.head("https://www.google.com", timeout=3)
        return True
    except requests.RequestException:
        return False

def check_dependencies():
    if not check_internet():
        print("No internet connection! Please check your internet connection.")
        input("Press Enter to exit...")
        sys.exit()

    if shutil.which("ffmpeg") is None:
        print("FFmpeg is not installed on your system. Please download it!")
        print("To download FFmpeg: (https://ffmpeg.org/download.html)")
        input("Press Enter to exit...")
        sys.exit()

    if find_spec("yt_dlp") is None:
        print("yt-dlp is not installed on the python system, please install it!")
        print("\nWindows/MacOS: pip install yt-dlp")
        print("Debian/Ubuntu: sudo apt install yt-dlp")
        print("Fedora/RHEL: sudo dnf install yt-dlp")
        print("Arch Linux: sudo pacman -S yt-dlp")
        print("OpenSUSE: sudo zypper install yt-dlp\n")
        input("Press Enter to exit...")
        sys.exit()

def check_ytdlp_version():
    try:
        local_version = importlib.metadata.version("yt_dlp")
        response = requests.get("https://pypi.org/pypi/yt-dlp/json", timeout=5)
        latest_version = response.json()["info"]["version"]

        if local_version < latest_version:
            print(f"!!! yt-dlp is not up to date! (Current: {local_version}, Latest: {latest_version}) !!!")
            choice = input("Would you like to update it now? (y/n): ").strip().lower()
            if choice == 'y':
                print("Updating yt-dlp...")
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True)
                print("yt-dlp has been updated. Please restart the script.")
                input("Press Enter to exit...")
                sys.exit()
    except Exception as e:
        print(f"Could not check for yt-dlp updates: {e}")

def get_valid_url():
    while True:
        url = input("Please enter the YouTube URL: ").strip()
        if "youtube" in url or "youtu.be" in url:
            if "live" in url:
                print("Live broadcasts cannot be downloaded!")
                continue
            return url
        else:
            print("This YouTube URL is invalid!")

def get_download_folder():
    while True:
        custom_path = input("Enter the folder to download to (leave blank for default 'Downloads' folder): ").strip()
        if not custom_path:
            return str(Path.home() / "Downloads")
        
        folder = Path(custom_path)
        if folder.exists() and folder.is_dir():
            return str(folder)
        else:
            print("Folder not found or is not a directory!")

def get_output_template(url, download_folder):
    if "playlist" in url:
        return f"{download_folder}/%(playlist_title)s/%(title)s.%(ext)s"
    else:
        return f"{download_folder}/%(title)s.%(ext)s"

def get_video_settings(outtmpl):
    while True:
        print("\nSelect video quality:")
        print("1 - 1080p/2160p (High)")
        print("2 - 720p (Medium)")
        print("3 - 480p (Low)")
        choice = input("Choice (leave blank for highest): ").strip()

        quality_map = {
            "1": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/mp4",
            "2": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/mp4",
            "3": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/mp4",
            "": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/mp4"
        }

        if choice in quality_map:
            return {
                "format": quality_map[choice],
                "postprocessors": [{"key": "FFmpegMetadata"}],
                "addmetadata": True,
                "outtmpl": outtmpl,
                "quiet": False,
            }
        else:
            print("Invalid selection!")

def get_audio_settings(outtmpl):
    return {
        "format": "bestaudio/best",
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "m4a", "preferredquality": "0"},
            {"key": "FFmpegMetadata"},
        ],
        "addmetadata": True,
        "outtmpl": outtmpl,
        "quiet": False,
    }

def main():
    check_dependencies()
    check_ytdlp_version()

    print("\n================")
    print("Media Downloader")
    print("================")

    while True:
        url = get_valid_url()
        download_folder = get_download_folder()
        outtmpl = get_output_template(url, download_folder)
        settings = None

        while True:
            print("\nPlease select the file format:")
            print("1 - Video")
            print("2 - Audio")
            choice = input("Choice (leave blank for video): ").strip()

            if choice == "1" or choice == "":
                settings = get_video_settings(outtmpl)
                break
            elif choice == "2":
                settings = get_audio_settings(outtmpl)
                break
            else:
                print("Invalid value, please enter 1 or 2!")
        
        try:
            with yt_dlp.YoutubeDL(settings) as ydl:
                ydl.download([url])
            print("\nDownload Complete!")
        except yt_dlp.utils.DownloadError as e:
            print(f"\nAn error occurred during download: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

        another = input("Do you want to download another file? (y/n): ").strip().lower()
        if another != 'y':
            break

    print("Exiting program.")
    input("Press Enter to exit...")
    sys.exit()

if __name__ == "__main__":
    main()
