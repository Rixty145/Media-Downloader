#!/bin/bash

set -e

if ! command -v brew &> /dev/null; then
    echo "Homebrew could not be found. It is required to install ffmpeg."
    echo "Please install Homebrew by following the instructions at https://brew.sh"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. It is required to install yt-dlp."
    echo "Please install Python from python.org."
    exit 1
fi

MISSING_YTDLP=0
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp is not installed."
    MISSING_YTDLP=1
fi

MISSING_FFMPEG=0
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed."
    MISSING_FFMPEG=1
fi

if [ $MISSING_YTDLP -eq 0 ] && [ $MISSING_FFMPEG -eq 0 ]; then
    echo "All required packages are already installed."
else
    echo "Installing missing packages..."
    
    if [ $MISSING_YTDLP -eq 1 ]; then
        echo "Installing yt-dlp..."
        python3 -m pip install --upgrade yt-dlp
    fi
    
    if [ $MISSING_FFMPEG -eq 1 ]; then
        echo "Installing ffmpeg..."
        brew install ffmpeg
    fi
fi

echo ""
echo "Setup complete."
