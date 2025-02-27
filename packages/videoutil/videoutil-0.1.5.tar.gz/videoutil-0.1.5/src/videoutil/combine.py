import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess
import logging
from datetime import datetime, timedelta

def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size

def format_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def format_time(seconds: float) -> str:
    """Format time duration in human readable format."""
    return str(timedelta(seconds=round(seconds)))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ensure_even(n: int) -> int:
    """Ensure number is even by rounding down if necessary."""
    return n - (n % 2)

def get_video_info(video_path: Path) -> Dict:
    """Get video dimensions and duration using ffprobe."""
    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-hide_banner'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    dimensions = re.search(r'Stream.*Video.* ([0-9]+)x([0-9]+)', result.stderr)
    if not dimensions:
        raise ValueError(f"Could not extract dimensions from {video_path}")
        
    width, height = map(int, dimensions.groups())
    duration = re.search(r'Duration: ([0-9]+):([0-9]+):([0-9]+)', result.stderr)
    if not duration:
        raise ValueError(f"Could not extract duration from {video_path}")
        
    h, m, s = map(int, duration.groups())
    duration_seconds = h * 3600 + m * 60 + s
    
    return {
        'width': width,
        'height': height,
        'duration': duration_seconds
    }

def get_quality_settings(quality: str) -> Dict[str, str]:
    """Get FFmpeg encoding settings based on quality level."""
    settings = {
        'high': {
            'preset': 'slower',
            'crf': '18'
        },
        'mid': {
            'preset': 'medium',
            'crf': '23'
        },
        'low': {
            'preset': 'faster',
            'crf': '28'
        }
    }
    return settings.get(quality.lower(), settings['mid'])

def calculate_size_scale(size: str) -> float:
    """Get scaling factor based on size setting."""
    scales = {
        'large': 1.0,    # 100%
        'mid': 0.75,     # 75%
        'small': 0.5     # 50%
    }
    return scales.get(size.lower(), 1.0)

def find_matching_pairs(directory: Path) -> List[Tuple[Path, Path]]:
    """Find matching A and B video pairs based on filename patterns."""
    video_files = list(directory.glob("*.[mM][pP]4"))
    
    # More flexible pattern matching for A and B videos
    a_videos = [v for v in video_files if " A." in v.name or "_A." in v.name]
    b_videos = [v for v in video_files if " B." in v.name or "_B." in v.name]
    
    logger.info(f"Found {len(a_videos)} A videos and {len(b_videos)} B videos")
    
    pairs = []
    for a_video in a_videos:
        # Try different possible B patterns
        b_name = a_video.name.replace(" A.", " B.")
        b_name2 = a_video.name.replace("_A.", "_B.")
        
        # Look for matching B video
        matching_b = next((b for b in b_videos if b.name == b_name or b.name == b_name2), None)
        
        if matching_b:
            pairs.append((a_video, matching_b))
            logger.info(f"Matched pair: {a_video.name} - {matching_b.name}")
        else:
            logger.warning(f"No matching B video found for {a_video}")
    
    return pairs

def process_video_pair(pair: Tuple[Path, Path], output_dir: Path, quality: str = 'mid', size: str = 'large') -> Tuple[float, Dict[str, int]]:
    """Process a single pair of videos with quality and size controls."""
    start_time = time.time()
    a_video, b_video = pair
    
    try:
        # Get video information
        a_info = get_video_info(a_video)
        b_info = get_video_info(b_video)
        
        # Apply size scaling
        scale_factor = calculate_size_scale(size)
        max_height = ensure_even(int(max(a_info['height'], b_info['height']) * scale_factor))
        
        # Calculate scaled widths maintaining aspect ratio and ensuring even numbers
        a_scaled_width = ensure_even(round((max_height / a_info['height']) * a_info['width']))
        b_scaled_width = ensure_even(round((max_height / b_info['height']) * b_info['width']))
        
        # Adjust scaled widths to ensure they're compatible with yuv420p
        a_scaled_width = max(2, ensure_even(a_scaled_width))
        b_scaled_width = max(2, ensure_even(b_scaled_width))
        
        # Get quality settings
        quality_settings = get_quality_settings(quality)
        
        # Create output filename
        output_name = f"{a_video.stem.replace(' A', '')}.mp4"
        output_path = output_dir / output_name
        
        # Log dimensions and processing info
        logger.info(f"Processing: {a_video.name} + {b_video.name} -> {output_path.name}")
        logger.info(f"Quality: {quality}, Size: {size}")
        logger.info(f"Scaling A: {a_info['width']}x{a_info['height']} -> {a_scaled_width}x{max_height}")
        logger.info(f"Scaling B: {b_info['width']}x{b_info['height']} -> {b_scaled_width}x{max_height}")
        
        # Build FFmpeg command
        cmd = [
            'ffmpeg', '-y',
            '-i', str(a_video),
            '-i', str(b_video),
            '-filter_complex',
            f'[0:v]scale={a_scaled_width}:{max_height}:force_original_aspect_ratio=decrease,setsar=1[scaled0];'
            f'[1:v]scale={b_scaled_width}:{max_height}:force_original_aspect_ratio=decrease,setsar=1[scaled1];'
            f'[scaled0]pad={a_scaled_width}:{max_height}:(ow-iw)/2:(oh-ih)/2[left];'
            f'[scaled1]pad={b_scaled_width}:{max_height}:(ow-iw)/2:(oh-ih)/2[right];'
            '[left][right]hstack=inputs=2,format=yuv420p[v]',
            '-map', '[v]',
            '-map', '1:a',
            '-c:v', 'libx265',
            '-preset', quality_settings['preset'],
            '-crf', quality_settings['crf'],
            '-tag:v', 'hvc1',
            '-pix_fmt', 'yuv420p',
            str(output_path)
        ]
        
        # Run FFmpeg process
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Always measure time right after FFmpeg finishes
        processing_time = time.time() - start_time
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            return processing_time, {'input_a': 0, 'input_b': 0, 'output': 0}
        
        # Get file sizes
        sizes = {
            'input_a': get_file_size(a_video),
            'input_b': get_file_size(b_video),
            'output': get_file_size(output_path)
        }
        
        logger.info(f"Successfully combined: {output_path.name}")
        return processing_time, sizes
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error processing {a_video.name} and {b_video.name}: {str(e)}")
        return processing_time, {'input_a': 0, 'input_b': 0, 'output': 0}

def combine_videos():
    while True:
        dir_input = input("Enter input directory path: ").strip()
        input_dir = Path(dir_input)
        if input_dir.exists() and input_dir.is_dir():
            break
        print(f"Error: '{dir_input}' is not a valid directory. Please try again.")
    
    # Get quality and size settings from user
    quality = input("Enter quality (high/mid/low, default: mid): ").strip().lower() or 'mid'
    if quality not in ['high', 'mid', 'low']:
        print(f"Invalid quality setting '{quality}', using 'mid'")
        quality = 'mid'
        
    size = input("Enter size (large/mid/small, default: large): ").strip().lower() or 'large'
    if size not in ['large', 'mid', 'small']:
        print(f"Invalid size setting '{size}', using 'large'")
        size = 'large'
    
    # Create output directory based on input name
    output_dir = Path(f"{input_dir}_output")
    
    print(f"Using input directory: {input_dir}")
    print(f"Using output directory: {output_dir}")
    print(f"Quality: {quality}")
    print(f"Size: {size}")
    
    # Verify input directory exists
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        pairs = find_matching_pairs(input_dir)
        if not pairs:
            print("No matching video pairs found!")
            return
            
        print(f"Found {len(pairs)} video pairs to process")
        
        # Track processing statistics
        total_start_time = time.time()
        processing_times = []
        total_input_size = 0
        total_output_size = 0
        
        # Process each pair
        for pair in pairs:
            print(f"\nProcessing: {pair[0].name} and {pair[1].name}")
            processing_time, sizes = process_video_pair(pair, output_dir, quality, size)
            
            # Update statistics
            processing_times.append(processing_time)
            total_input_size += sizes['input_a'] + sizes['input_b']
            total_output_size += sizes['output']
            
            # Print individual statistics
            print(f"Individual processing time: {format_time(processing_time)}")
            print(f"Input sizes: A={format_size(sizes['input_a'])}, B={format_size(sizes['input_b'])}")
            print(f"Output size: {format_size(sizes['output'])}")
            compression_ratio = (sizes['input_a'] + sizes['input_b']) / sizes['output'] if sizes['output'] > 0 else 0
            print(f"Compression ratio: {compression_ratio:.2f}x")
        
        # Calculate and print overall statistics
        total_time = time.time() - total_start_time
        avg_time = sum(processing_times) / len(processing_times)
        
        print("\n=== Overall Statistics ===")
        print(f"Total processing time: {format_time(total_time)}")
        print(f"Average time per video: {format_time(avg_time)}")
        print(f"Total input size: {format_size(total_input_size)}")
        print(f"Total output size: {format_size(total_output_size)}")
        print(f"Overall compression ratio: {total_input_size/total_output_size:.2f}x" if total_output_size > 0 else "Overall compression ratio: N/A")
        print(f"Space saved: {format_size(total_input_size - total_output_size)}")
        print(f"Output files are in: {output_dir}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    combine_videos()