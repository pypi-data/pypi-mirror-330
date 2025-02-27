import os
import subprocess
import time

def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

def compress_videos():
    # Ask for the input directory
    input_dir = input("Enter the directory containing videos to compress: ").strip()
    if not os.path.isdir(input_dir):
        print(f"The directory '{input_dir}' does not exist.")
        return

    # Ask for resolution shrink percentage
    resolution = input("Enter resolution shrinking percentage (high=100, mid=75, low=50, default: high): ").strip().lower() or 'high'
    resolution_map = {'high': 1.0, 'mid': 0.75, 'low': 0.5}
    if resolution not in resolution_map:
        print(f"Invalid resolution setting '{resolution}', using 'high'")
        resolution = 'high'
    scaling_factor = resolution_map[resolution]

    # Ask for quality (crf)
    quality = input("Enter quality (high/mid/low, default: mid): ").strip().lower() or 'mid'
    settings = {
        'high': {'preset': 'slower', 'crf': 18},
        'mid': {'preset': 'medium', 'crf': 23},
        'low': {'preset': 'faster', 'crf': 28},
    }
    if quality not in settings:
        print(f"Invalid quality setting '{quality}', using 'mid'")
        quality = 'mid'

    # Create the output directory
    output_dir = input_dir.rstrip('/') + "_output"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize statistics
    total_input_size = 0
    total_output_size = 0
    processing_times = []

    total_start_time = time.time()

    # Compress each video in the input directory
    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        if not os.path.isfile(input_path) or not file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):
            continue

        output_path = os.path.join(output_dir, file_name)
        scale_filter = f"scale=iw*{scaling_factor}:ih*{scaling_factor}"

        # Record file sizes
        input_size = os.path.getsize(input_path)
        total_input_size += input_size

        # Start timer for processing
        start_time = time.time()

        # Run FFmpeg command
        ffmpeg_cmd = [
            "ffmpeg", "-i", input_path,
            "-vf", scale_filter,
            "-c:v", "libx265",
            "-vtag", "hvc1",
            "-crf", str(settings[quality]['crf']),
            "-preset", settings[quality]['preset'],
            "-c:a", "aac",
            output_path
        ]
        print(f"Processing '{file_name}'...")
        subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # End timer and calculate stats
        processing_time = time.time() - start_time
        processing_times.append(processing_time)
        output_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
        total_output_size += output_size

        # Print individual statistics
        print(f"Individual processing time: {format_time(processing_time)}")
        print(f"Input size: {format_size(input_size)}")
        print(f"Output size: {format_size(output_size)}")
        compression_ratio = input_size / output_size if output_size > 0 else 0
        print(f"Compression ratio: {compression_ratio:.2f}x\n")

    # Calculate and print overall statistics
    total_time = time.time() - total_start_time
    avg_time = sum(processing_times) / len(processing_times) if processing_times else 0

    print("\n=== Overall Statistics ===")
    print(f"Total processing time: {format_time(total_time)}")
    print(f"Average time per video: {format_time(avg_time)}")
    print(f"Total input size: {format_size(total_input_size)}")
    print(f"Total output size: {format_size(total_output_size)}")
    print(f"Overall compression ratio: {total_input_size/total_output_size:.2f}x" if total_output_size > 0 else "Overall compression ratio: N/A")
    print(f"Space saved: {format_size(total_input_size - total_output_size)}")
    print(f"Output files are in: {output_dir}")

if __name__ == "__main__":
    compress_videos()