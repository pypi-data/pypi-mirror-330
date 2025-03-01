# STREAMIX
Streamix is a lightweight and efficient Python tool for downloading videos and audio from YouTube. With customizable quality options and seamless integration with yt-dlp and FFmpeg, Streamix empowers you to save your favorite content in no time. 🚀

## Features
- Download both video and audio together in MP4 format.
- Choose from a range of video quality options: 240p, 360p, 480p, 720p, and 1080p.
- Extract high-quality audio in formats like MP3 and AAC.
- Optimized for speed with features like concurrent downloads and chunked HTTP requests.
- Easy-to-use CLI (Command Line Interface).
- Easy-to-use interface for both video and audio downloading.

## Installation
- First, make sure Python 3.6 or higher is installed on your system.
- Open your terminal or command prompt.
- Install the tool via pip:
```bash
  pip install streamix
```
- You're all set! Just type streamix in your terminal to use it.

## Usage
After installation, you can start Streamix from the command line using:
```bash 
  streamix
}
```
Once launched, you'll see a menu with the following options:
- Download Video
- Download Audio

For video downloading, you can choose from the following quality options:
- 240p
- 360p
- 480p
- 720p
- 1080p

Input the desired YouTube URL after choosing your download option, and Streamix will download the video or audio for you!

## Requirements
- Python 3.6 or higher
- pip, the Python package manager.
- Optional: ffmpeg for enhanced video/audio processing.

Install ffmpeg via:
- ### Linux: 
sudo apt install ffmpeg
- ### Windows: 
Download from ffmpeg.org

## Error Handling
### Invalid URL: 
- "An error occurred: Invalid URL. Please enter a valid YouTube URL."
### Missing ffmpeg:
- "An error occurred: ffmpeg not found. Please install or configure ffmpeg."
### Network Issues:
- "An error occurred: Network error" indicate connectivity problems.

## Setup
Streamix uses yt-dlp for downloading content, which is a fork of youtube-dl and supports downloading from many video and audio platforms.

## Developer Information
- Author: Tanisha Jain
- Email: itanishajain@gmail.com
- Linkedin: https://www.linkedin.com/in/itanishajain/
- GitHub: https://github.com/itanishajain/StreamIX

## Feedback
If you have anyissues or feedback, please reach out to us at itanishajain@gmail.com