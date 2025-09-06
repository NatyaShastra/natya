import os
import cv2
import subprocess
import numpy as np

def downscale_video(input_path, output_path=None, target_width=640, target_height=None, method='ffmpeg'):
    """
    Downscale a video to a smaller resolution for faster processing.
    
    Args:
        input_path (str): Path to the input video file
        output_path (str, optional): Path to save the downscaled video. If None, uses input_path + '_downscaled.mp4'
        target_width (int): Target width for the downscaled video. Default is 640px.
        target_height (int, optional): Target height. If None, maintains aspect ratio
        method (str): Method to use for downscaling ('ffmpeg' or 'opencv'). Default is 'ffmpeg'.
        
    Returns:
        str: Path to the downscaled video if successful, original path if failed
    """
    if not os.path.exists(input_path):
        print(f"Error: Input video file does not exist: {input_path}")
        return input_path
        
    # If output_path is not specified, create one
    if output_path is None:
        filename, ext = os.path.splitext(input_path)
        output_path = f"{filename}_downscaled{ext}"
    
    try:
        # Get original video dimensions
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video: {input_path}")
            return input_path
        
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        # Calculate target height if not specified (maintain aspect ratio)
        if target_height is None:
            target_height = int(original_height * (target_width / original_width))
            # Ensure height is even (required for some codecs)
            if target_height % 2 != 0:
                target_height += 1
        
        # Skip if the video is already smaller than target size
        if original_width <= target_width and original_height <= target_height:
            print(f"Video is already at or below target resolution. Skipping downscale.")
            return input_path
        
        print(f"Downscaling video from {original_width}x{original_height} to {target_width}x{target_height}")
        
        if method == 'ffmpeg':
            # Use ffmpeg for downscaling (fast and efficient)
            cmd = [
                'ffmpeg', '-y',  # Overwrite output files
                '-i', input_path,
                '-vf', f'scale={target_width}:{target_height}',
                '-c:v', 'libx264',  # H.264 codec
                '-preset', 'fast',  # Fast encoding
                '-crf', '23',  # Quality (lower = better)
                '-c:a', 'copy',  # Copy audio stream
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error downscaling video with ffmpeg: {result.stderr}")
                return input_path
                
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"Successfully downscaled video: {output_path}")
                return output_path
            else:
                print(f"Failed to create downscaled video")
                return input_path
                
        elif method == 'opencv':
            # Use OpenCV for downscaling (more control but slower)
            in_cap = cv2.VideoCapture(input_path)
            fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec
            out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))
            
            while in_cap.isOpened():
                ret, frame = in_cap.read()
                if not ret:
                    break
                
                # Resize frame
                resized_frame = cv2.resize(frame, (target_width, target_height))
                out.write(resized_frame)
            
            in_cap.release()
            out.release()
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"Successfully downscaled video: {output_path}")
                return output_path
            else:
                print(f"Failed to create downscaled video")
                return input_path
        else:
            print(f"Unknown downscaling method: {method}")
            return input_path
            
    except Exception as e:
        print(f"Error downscaling video: {e}")
        return input_path