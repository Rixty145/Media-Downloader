#!/bin/bash

if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Distribution could not be detected. Please perform a manual installation."
    exit 1
fi

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

install_packages() {
    case "$DISTRO" in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y python3-pip ffmpeg
            python3 -m pip install --upgrade yt-dlp
            ;;
        fedora)
            sudo dnf install -y python3-pip ffmpeg
            python3 -m pip install --upgrade yt-dlp
            ;;
        arch)
            sudo pacman -Syu --noconfirm python-pip ffmpeg
            python3 -m pip install --upgrade yt-dlp
            ;;
        opensuse-leap|sles)
            sudo zypper install -y python3-pip ffmpeg
            python3 -m pip install --upgrade yt-dlp
            ;;
        *)
            echo "Automatic installation is not supported for this distribution. Please perform a manual installation."
            exit 1
            ;;
    esac
}

MISSING=0
if ! command_exists yt-dlp; then
    echo "yt-dlp is not installed."
    MISSING=1
fi

if ! command_exists ffmpeg; then
    echo "ffmpeg is not installed."
    MISSING=1
fi

if [ $MISSING -eq 1 ]; then
    echo "Installing missing packages..."
    install_packages
else
    echo "All required packages are already installed."
fi

echo "Setup complete."