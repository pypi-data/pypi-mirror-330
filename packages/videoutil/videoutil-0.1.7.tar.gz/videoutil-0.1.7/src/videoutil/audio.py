import os
import time
import subprocess
import sys
import click  # if using click in your CLI; otherwise plain input/print works fine

def format_time(seconds):
    """Convert seconds to hh:mm:ss format."""
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def get_video_duration(video_path):
    """
    Use ffprobe to get the total duration (in seconds) of the video.
    Returns 0.0 if the duration cannot be determined.
    """
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return 0.0
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0

def parse_hhmmss(timestr):
    """
    Parse a time string in hh:mm:ss.xxx format into total seconds.
    E.g., "00:02:03.45" -> 123.45 seconds.
    """
    parts = timestr.split(':')
    if len(parts) != 3:
        return 0.0
    try:
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return 0.0

def run_ffmpeg_with_progress(ffmpeg_cmd, total_duration, label):
    """
    Run the given ffmpeg command with progress reporting.
    ffmpeg_cmd should include "-progress pipe:1 -nostats" at the end.
    total_duration is used to compute a progress percentage.
    label is a string identifier (e.g., filename) to display with progress.
    """
    proc = subprocess.Popen(
        ffmpeg_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    processed_seconds = 0.0
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        line = line.strip()
        if line.startswith("out_time_ms="):
            try:
                ms = float(line.split("=")[1])
                processed_seconds = ms / 1000000.0
            except ValueError:
                pass
        elif line.startswith("out_time="):
            time_str = line.split("=")[1].strip()
            processed_seconds = parse_hhmmss(time_str)
        progress_percent = (processed_seconds / total_duration) * 100 if total_duration > 0 else 0
        if progress_percent > 100:
            progress_percent = 100
        print(f"{label} Progress: {progress_percent:5.2f}%", end="\r")
        sys.stdout.flush()
    proc.wait()
    return proc.returncode, proc.stderr.read()

def adjust_audio():
    """Adjust the volume and apply optional filters to all video files in a directory."""
    input_dir = input("Enter the directory containing video files for audio adjustment: ").strip()
    if not os.path.isdir(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist.")
        return
    input_dir = os.path.abspath(input_dir)

    print("Volume adjustment options:")
    print("1: Lower to 10%")
    print("2: Lower to 25%")
    print("3: Lower to 50%")
    print("4: Increase to 200%")
    print("5: Increase to 400%")
    print("6: Increase to 1000%")
    choice = input("Enter your choice (1-6): ").strip()

    volume_map = {
        "1": 0.1,
        "2": 0.25,
        "3": 0.5,
        "4": 2.0,
        "5": 4.0,
        "6": 10.0
    }
    if choice not in volume_map:
        print("Invalid choice. Exiting.")
        return
    volume_factor = volume_map[choice]

    print("\nOptional audio filters:")
    print("1: Low-pass filter at 3,000 Hz (reduce high-frequency noise)")
    print("2: High-pass filter at 300 Hz (reduce low-frequency noise)")
    print("3: High-pass filter at 50 Hz (remove hum and very low rumble)")
    print("4: Low-pass filter at 8,000 Hz (preserve more speech clarity while reducing noise)")
    print("5: No filter (default)")
    filter_choice = input("Enter your choice (1-5): ").strip()

    filter_map = {
        "1": "lowpass=f=3000",
        "2": "highpass=f=300",
        "3": "highpass=f=50",
        "4": "lowpass=f=8000",
        "5": None
    }
    if filter_choice not in filter_map:
        print("Invalid filter choice. No filter will be applied.")
        filter_choice = "5"
    audio_filter = filter_map[filter_choice]
    
    audio_filter_string = f"volume={volume_factor}"
    if audio_filter:
        audio_filter_string += f",{audio_filter}"

    output_dir = input_dir.rstrip('/') + "_output"
    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        if not os.path.isfile(input_path) or not file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):
            continue
        duration = get_video_duration(input_path)
        if duration <= 0:
            print(f"Could not determine duration for {file_name}. Skipping.")
            continue
        output_path = os.path.join(output_dir, file_name)
        ffmpeg_cmd = [
            "ffmpeg", "-i", input_path,
            "-c:v", "copy",
            "-af", audio_filter_string,
            output_path,
            "-y"
        ]
        progress_cmd = ffmpeg_cmd[:] + ["-progress", "pipe:1", "-nostats"]

        print(f"\nProcessing '{file_name}' for audio adjustment...")
        retcode, stderr_data = run_ffmpeg_with_progress(progress_cmd, duration, file_name)
        print()  # newline after progress
        if retcode == 0 and os.path.exists(output_path):
            print(f"Adjusted audio saved at: {output_path}")
        else:
            print(f"Error: Failed to adjust audio for '{file_name}'.")
            print(stderr_data)

    print(f"\nProcessing complete. Adjusted files saved in: {output_dir}")

def extract_audio():
    """Extract the audio track from all video files in a directory with an option to copy or re-encode."""
    input_dir = input("Enter the directory containing video files to extract audio from: ").strip()
    if not os.path.isdir(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist.")
        return
    input_dir = os.path.abspath(input_dir)
    output_dir = input_dir.rstrip('/') + "_audio_output"
    os.makedirs(output_dir, exist_ok=True)

    print("Audio Extraction Options:")
    print("1: Copy audio stream (fastest; no re-encoding)")
    print("2: Re-encode to MP3 (for compatibility)")
    choice = input("Enter your choice (1 or 2): ").strip()

    # Process each video file in the directory
    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        if not os.path.isfile(input_path) or not file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):
            continue

        duration = get_video_duration(input_path)
        if duration <= 0:
            print(f"Could not determine duration for {file_name}. Skipping.")
            continue

        base, _ = os.path.splitext(file_name)
        if choice == "1":
            # Copy audio stream. We'll output as .m4a (common for AAC).
            output_file = base + "_audio.m4a"
            output_path = os.path.join(output_dir, output_file)
            ffmpeg_cmd = [
                "ffmpeg", "-i", input_path,
                "-vn",
                "-c:a", "copy",
                output_path,
                "-y"
            ]
        elif choice == "2":
            # Re-encode to MP3.
            output_file = base + "_audio.mp3"
            output_path = os.path.join(output_dir, output_file)
            ffmpeg_cmd = [
                "ffmpeg", "-i", input_path,
                "-vn",
                "-ar", "44100",
                "-ac", "2",
                "-b:a", "192k",
                output_path,
                "-y"
            ]
        else:
            print("Invalid choice. Skipping extraction for this file.")
            continue

        progress_cmd = ffmpeg_cmd[:] + ["-progress", "pipe:1", "-nostats"]

        print(f"\nExtracting audio from '{file_name}'...")
        retcode, stderr_data = run_ffmpeg_with_progress(progress_cmd, duration, file_name)
        print()  # newline after progress
        if retcode == 0 and os.path.exists(output_path):
            print(f"Extracted audio saved at: {output_path}")
        else:
            print(f"Error: Failed to extract audio for '{file_name}'.")
            print(stderr_data)

    print(f"\nAudio extraction complete. Files saved in: {output_dir}")

def audio_main():
    """Prompt the user to choose an audio operation."""
    print("Audio Processing Options:")
    print("1: Adjust audio (volume and filters)")
    print("2: Extract audio track")
    choice = input("Enter your choice (1 or 2): ").strip()
    if choice == "1":
        adjust_audio()
    elif choice == "2":
        extract_audio()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    audio_main()