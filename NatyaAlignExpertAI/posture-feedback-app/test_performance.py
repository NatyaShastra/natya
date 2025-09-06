#!/usr/bin/env python3
"""
Test script to measure performance improvements in the posture feedback system.
This script processes the same video with different optimization settings and
measures the processing time for each configuration.
"""

import os
import time
import sys
import subprocess
import argparse
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from feedback_generator import FeedbackGenerator
from utils.video_utils import downscale_video

def time_function(func, *args, **kwargs):
    """Measure the execution time of a function"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    duration = end_time - start_time
    return duration, result

def main():
    parser = argparse.ArgumentParser(description='Test the performance of posture feedback system')
    parser.add_argument('--video', type=str, default='uploads/student1.mp4', 
                        help='Path to the test video file')
    parser.add_argument('--model', type=str, 
                        default='/workspaces/natya/NatyaAlignExpertAI/posture-feedback-app/trained_model/model_generated.pkl',
                        help='Path to the model file')
    parser.add_argument('--step', type=str, default='Bharatanatyam Araimandi',
                        help='Dance step to use for testing')
    args = parser.parse_args()
    
    video_path = args.video
    model_path = args.model
    dance_step = args.step
    
    # Check if the video exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return
    
    print(f"Performance test using video: {video_path}")
    print(f"Model: {model_path}")
    print(f"Dance step: {dance_step}")
    print("-" * 50)
    
    # Get video information
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,duration,codec_name,r_frame_rate',
        '-of', 'default=noprint_wrappers=1',
        video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Video information:\n{result.stdout}")
    print("-" * 50)
    
    # Create a directory for test outputs
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the feedback generator
    generator = FeedbackGenerator(model_path)
    
    # Test configurations
    configs = [
        {"name": "Baseline (no optimizations)", "sample_rate": 1, "downscale": False, "width": None},
        {"name": "Frame sampling only (3)", "sample_rate": 3, "downscale": False, "width": None},
        {"name": "Frame sampling only (5)", "sample_rate": 5, "downscale": False, "width": None},
        {"name": "Downscale only (640px)", "sample_rate": 1, "downscale": True, "width": 640},
        {"name": "Downscale only (480px)", "sample_rate": 1, "downscale": True, "width": 480},
        {"name": "Combined optimizations (3, 640px)", "sample_rate": 3, "downscale": True, "width": 640},
        {"name": "Combined optimizations (5, 480px)", "sample_rate": 5, "downscale": True, "width": 480},
        {"name": "Maximum optimization (10, 320px)", "sample_rate": 10, "downscale": True, "width": 320},
    ]
    
    results = []
    
    for config in configs:
        print(f"\nTesting configuration: {config['name']}")
        
        # Prepare test video (downscale if needed)
        test_video = video_path
        if config['downscale'] and config['width']:
            print(f"Downscaling video to {config['width']}px width...")
            video_name = Path(video_path).stem
            downscaled_path = os.path.join(output_dir, f"{video_name}_w{config['width']}.mp4")
            test_video = downscale_video(video_path, downscaled_path, target_width=config['width'])
            print(f"Downscaled video saved to: {test_video}")
        
        # Process the video and measure time
        output_path = os.path.join(output_dir, f"output_{config['name'].replace(' ', '_')}.mp4")
        print(f"Processing with frame_sample_rate={config['sample_rate']}...")
        
        duration, (result_path, feedback) = time_function(
            generator.annotate_video_with_feedback,
            test_video,
            output_path,
            dance_step,
            config['sample_rate']
        )
        
        # Record results
        config['duration'] = duration
        config['output_path'] = result_path
        config['feedback'] = feedback
        
        print(f"Processing time: {duration:.2f} seconds")
        if result_path:
            print(f"Output video: {result_path}")
        else:
            print("Failed to create output video")
        
        results.append(config)
    
    # Print summary
    print("\n" + "=" * 80)
    print("PERFORMANCE TEST RESULTS")
    print("=" * 80)
    print(f"{'Configuration':<40} {'Duration (s)':<15} {'Speedup':<10}")
    print("-" * 80)
    
    baseline_duration = results[0]['duration']
    
    for result in results:
        speedup = baseline_duration / result['duration'] if result['duration'] > 0 else 0
        print(f"{result['name']:<40} {result['duration']:.2f}s{' ':<8} {speedup:.2f}x")
    
    print("\nDETAILED CONFIGURATION INFORMATION:")
    for result in results:
        print(f"\n{result['name']}:")
        print(f"  - Frame sample rate: {result['sample_rate']}")
        print(f"  - Downscaling: {'Yes' if result['downscale'] else 'No'}")
        if result['downscale'] and result['width']:
            print(f"  - Target width: {result['width']}px")
        print(f"  - Processing time: {result['duration']:.2f} seconds")
        print(f"  - Speedup: {baseline_duration / result['duration']:.2f}x")
        print(f"  - Output video: {result['output_path'] if result['output_path'] else 'Failed'}")
        print(f"  - Feedback: {result['feedback']}")

if __name__ == "__main__":
    main()