import os
import subprocess
import tempfile
import shutil
import cv2

def generate_video_with_ffmpeg(frames_dir, output_path, fps=30):
    """
    Generate a video from a directory of frames using ffmpeg.
    
    Args:
        frames_dir: Directory containing the frames
        output_path: Path where the output video will be saved
        fps: Frames per second for the output video
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Construct the ffmpeg command
        cmd = [
            'ffmpeg', '-y',  # Force overwrite
            '-framerate', str(fps),
            '-i', os.path.join(frames_dir, 'frame_%04d.jpg'),  # Input pattern
            '-c:v', 'libx264',  # Use H.264 codec
            '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
            '-preset', 'fast',  # Encoding speed/quality tradeoff
            '-crf', '22',  # Quality (lower is better, 18-28 is usual range)
            output_path
        ]
        
        # Run the command
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # Check if output file exists and has non-zero size
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Successfully created video with ffmpeg: {output_path}")
            return True
        else:
            print(f"ffmpeg command completed but video file not created properly")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"Error in generate_video_with_ffmpeg: {str(e)}")
        return False

def cv2_frames_to_ffmpeg_video(frames, output_path, fps=30):
    """
    Convert OpenCV frames to a video using ffmpeg.
    
    Args:
        frames: List of numpy arrays representing frames
        output_path: Path where the output video will be saved
        fps: Frames per second for the output video
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create a temporary directory to store frames
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save frames as images
            for i, frame in enumerate(frames):
                frame_path = os.path.join(temp_dir, f"frame_{i:04d}.jpg")
                cv2.imwrite(frame_path, frame)
                
            # Generate video from the frames
            return generate_video_with_ffmpeg(temp_dir, output_path, fps)
    except Exception as e:
        print(f"Error in cv2_frames_to_ffmpeg_video: {str(e)}")
        return False

def ensure_min_duration(video_path, min_duration=10.0):
    """
    Ensure that a video meets a minimum duration by extending it if needed.
    
    Args:
        video_path: Path to the video file
        min_duration: Minimum duration in seconds
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get the current duration using ffprobe
        probe_cmd = [
            "ffprobe", 
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        
        result = subprocess.run(probe_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error checking video duration: {result.stderr}")
            return False
            
        current_duration = float(result.stdout.strip())
        
        # If already meets minimum duration, return success
        if current_duration >= min_duration:
            print(f"Video {video_path} already exceeds minimum duration ({min_duration:.2f}s)")
            return True
            
        # Calculate how much we need to extend
        extend_duration = min_duration - current_duration
        print(f"Extending video {video_path} from {current_duration:.2f}s to {min_duration:.2f}s")
        
        # Create a temporary file for the extended video
        temp_output = f"{video_path}.temp.mp4"
        
        # Extend the video by adding a still frame at the end
        # This command extracts the last frame, freezes it for the needed duration, and concatenates
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"tpad=stop_mode=clone:stop_duration={extend_duration}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-pix_fmt", "yuv420p",
            temp_output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error extending video: {result.stderr}")
            return False
            
        # Replace the original video with the extended one
        os.replace(temp_output, video_path)
        
        # Verify the new duration
        result = subprocess.run(probe_cmd, capture_output=True, text=True)
        new_duration = float(result.stdout.strip())
        print(f"New video duration: {new_duration:.2f}s")
        
        return new_duration >= min_duration
        
    except Exception as e:
        print(f"Error in ensure_min_duration: {e}")
        return False