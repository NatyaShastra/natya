import os
import glob
from ffmpeg_utils import ensure_min_duration

def get_video_duration(video_path):
    """Get the duration of a video using ffprobe"""
    import subprocess
    import json
    
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'json',
        video_path
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print(f"Error getting video duration: {result.stderr}")
        return None
    
    try:
        data = json.loads(result.stdout)
        duration = float(data['format']['duration'])
        return duration
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing video duration: {e}")
        return None

def process_all_videos_in_directory(directory, min_duration=10.0):
    """Process all .mp4 files in a directory to ensure minimum duration"""
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return 0
        
    processed = 0
    
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            filepath = os.path.join(directory, filename)
            if ensure_min_duration(filepath, min_duration):
                processed += 1
    
    print(f"Processed {processed} videos in {directory}")
    print("Video processing complete - all videos now have minimum 10 second duration")
    return processed
    
# Keep the original function for backward compatibility
def extend_video_if_needed(video_path, min_duration=10.0):
    """Extend video to minimum duration if needed by adding freeze frames at the end"""
    return ensure_min_duration(video_path, min_duration)