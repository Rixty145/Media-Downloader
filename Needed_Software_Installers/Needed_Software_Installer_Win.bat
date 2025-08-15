@echo off
setlocal

where /q python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH. It is required for yt-dlp.
    echo Please install Python from python.org and ensure "Add to PATH" is checked.
    goto :end
)

where /q winget >nul 2>&1
if %errorlevel% neq 0 (
    echo winget command not found. It is required for ffmpeg.
    echo Please install the "App Installer" from the Microsoft Store.
    goto :end
)

set MISSING_YTDLP=0
where /q yt-dlp >nul 2>&1
if %errorlevel% neq 0 (
    echo yt-dlp is not installed.
    set MISSING_YTDLP=1
)

set MISSING_FFMPEG=0
where /q ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo ffmpeg is not installed.
    set MISSING_FFMPEG=1
)

if %MISSING_YTDLP% equ 0 if %MISSING_FFMPEG% equ 0 (
    echo All required packages are already installed.
) else (
    echo Installing missing packages...
    if %MISSING_YTDLP% equ 1 (
        python -m pip install --upgrade yt-dlp
    )
    if %MISSING_FFMPEG% equ 1 (
        winget install --id=Gyan.FFmpeg -e --source winget
    )
)

echo.
echo Setup complete.

:end
pause
endlocal