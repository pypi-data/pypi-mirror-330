import os
import sys
import subprocess

def get_ffmpeg_path():
    """
    Attempt to locate the FFmpeg executable on the system.
    Returns the path to FFmpeg if found, otherwise None.
    """
    try:
        # Check if ffmpeg is in PATH
        if sys.platform.startswith('win'):
            # On Windows
            try:
                result = subprocess.run(['where', 'ffmpeg'], 
                                       capture_output=True, 
                                       text=True, 
                                       check=True)
                if result.stdout.strip():
                    return result.stdout.strip().split('\n')[0]
            except subprocess.CalledProcessError:
                pass
        else:
            # On Unix-like systems
            try:
                result = subprocess.run(['which', 'ffmpeg'], 
                                       capture_output=True, 
                                       text=True, 
                                       check=True)
                if result.stdout.strip():
                    return result.stdout.strip()
            except subprocess.CalledProcessError:
                pass
        
        # If not found in PATH, return None
        print("FFmpeg not found in system PATH.")
        return None
    except Exception as e:
        print(f"Error finding FFmpeg: {e}")
        return None