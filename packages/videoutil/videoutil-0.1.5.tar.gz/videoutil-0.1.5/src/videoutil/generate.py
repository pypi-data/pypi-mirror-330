# src/videoutil/generate.py
import subprocess
from pathlib import Path

def create_test_video(output_path: Path, width: int, height: int, duration: int, text: str, is_b_video: bool = False):
    """Create a test video with specified dimensions and text."""
    
    # Prepare audio input based on video type
    if is_b_video:
        # Create a beeping sound for B videos using tone
        audio_input = '-f lavfi -i "aevalsrc=\'sin(2*PI*1000*t)\':d=10"'
    else:
        # White noise for A videos
        audio_input = '-f lavfi -i "aevalsrc=random(0):d=10"'
    
    # Construct the full FFmpeg command
    cmd = f'ffmpeg -y '  # Start with basic FFmpeg call
    cmd += f'-f lavfi -i "color=c=blue:s={width}x{height}:d={duration}" '  # Video input
    cmd += f'{audio_input} '  # Audio input
    cmd += f'-vf "drawtext=text=\'{text}\':fontsize={height//4}:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" '  # Add text
    cmd += f'-c:v libx264 -t {duration} '  # Video codec and duration
    cmd += f'-c:a aac -ar 44100 '  # Audio codec and sample rate
    cmd += f'"{str(output_path)}"'  # Output file
    
    print(f"Creating video: {output_path.name} ({width}x{height}, {duration}s)")
    
    try:
        # Run the command
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg command: {e}")
        raise

def generate_videos():
    """Generate test video pairs."""
    output_dir_str = input("Enter output directory path: ").strip()
    output_dir = Path(output_dir_str)
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Test video pairs with different dimensions and durations
    test_pairs = [
        {
            'A': {'width': 1072, 'height': 606, 'duration': 5},  # 5 seconds
            'B': {'width': 1024, 'height': 576, 'duration': 6},  # 6 seconds
            'name': 'test1'
        },
        {
            'A': {'width': 1024, 'height': 576, 'duration': 15},  # 15 seconds
            'B': {'width': 1366, 'height': 768, 'duration': 20},  # 20 seconds
            'name': 'test2'
        },
        {
            'A': {'width': 736, 'height': 414, 'duration': 30},   # 30 seconds
            'B': {'width': 1024, 'height': 576, 'duration': 35},  # 35 seconds
            'name': 'test3'
        }
    ]
    
    # Generate test videos
    for pair in test_pairs:
        # Create A video
        a_path = output_dir / f"{pair['name']} A.mp4"
        create_test_video(
            a_path,
            pair['A']['width'],
            pair['A']['height'],
            pair['A']['duration'],
            f"A {pair['A']['width']}x{pair['A']['height']}",
            is_b_video=False
        )
        print(f"Created: {a_path}")
        
        # Create B video
        b_path = output_dir / f"{pair['name']} B.mp4"
        create_test_video(
            b_path,
            pair['B']['width'],
            pair['B']['height'],
            pair['B']['duration'],
            f"B {pair['B']['width']}x{pair['B']['height']}",
            is_b_video=True
        )
        print(f"Created: {b_path}")

if __name__ == "__main__":
    generate_videos()