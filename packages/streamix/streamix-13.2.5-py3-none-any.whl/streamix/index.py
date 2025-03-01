import sys
import os
import yt_dlp
from utils import get_ffmpeg_path

# Function to get the Desktop path
def get_desktop_path():
    """Get the user's Desktop path."""
    try:
        # Expand user's home directory
        home_path = os.path.expanduser("~")
        print(f"Resolved Home Path: {home_path}")  # Debug
        
        # Construct the Desktop path
        desktop_path = os.path.join(home_path, "Desktop")
        print(f"Constructed Desktop Path: {desktop_path}")  # Debug
        
        # Check if the Desktop path exists
        if os.path.exists(desktop_path):
            return desktop_path
        else:
            raise FileNotFoundError("Desktop path does not exist.")
    except Exception as e:
        print(f"Error resolving Desktop path: {e}")
        return None

# Function to get the default Downloads path as a fallback
def get_default_download_path():
    """Get the default Downloads path as a fallback."""
    try:
        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        print(f"Default Downloads Path: {default_download_path}")  # Debug
        return default_download_path
    except Exception as e:
        print(f"Error resolving default download path: {e}")
        return None

# Function to download video
def download_video(url, quality):
    try:
        # Get Downloads path (Desktop as priority)
        download_path = get_desktop_path() or get_default_download_path()
        if not download_path:
            raise Exception("Unable to resolve Downloads path.")

        # Prepare yt-dlp options
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'merge_output_format': 'mp4',
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            },
        }

        # Check if FFmpeg is available
        ffmpeg_path = get_ffmpeg_path()
        if ffmpeg_path:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        else:
            print("Warning: FFmpeg is not installed. Video and audio may not be merged.")

        print(f"Output path template: {ydl_opts['outtmpl']}")  # Debug

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from {url}...")
            ydl.download([url])
        print(f"Video downloaded successfully to {download_path}!")
    except Exception as e:
        print(f"An error occurred during video download: {e}")

# Function to download audio
def download_audio(url):
    try:
        # Get Downloads path (Desktop as priority)
        download_path = get_desktop_path() or get_default_download_path()
        if not download_path:
            raise Exception("Unable to resolve Downloads path.")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'geo_bypass': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if get_ffmpeg_path() else None
        }

        if not get_ffmpeg_path():
            print("Warning: FFmpeg is not installed. Audio may not be converted to MP3 format.")

        print(f"Output path template: {ydl_opts['outtmpl']}")  # Debug

        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from {url}...")
            ydl.download([url])
        print(f"Audio downloaded successfully to {download_path}!")
    except Exception as e:
        print(f"An error occurred during audio download: {e}")

# Main function
def main():
    print("Welcome to Streamix!")
    print("1. Download Video")
    print("2. Download Audio")

    choice = input("Choose an option (1/2): ").strip()

    if choice == '1':
        print("Video Quality Options:")
        print("1. 240p\n2. 360p\n3. 480p\n4. 720p\n5. 1080p")
        quality_map = {'1': '240', '2': '360', '3': '480', '4': '720', '5': '1080'}
        quality = quality_map.get(input("Select quality (1-5): ").strip(), '720')
        url = input("Enter the YouTube URL: ").strip()
        download_video(url, quality)

    elif choice == '2':
        url = input("Enter the YouTube URL: ").strip()
        download_audio(url)
    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    main()