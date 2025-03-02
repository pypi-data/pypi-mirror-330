import os
import time
import subprocess
import sys

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

def split_videos():
    # 1. Ask for the directory containing video files.
    input_dir = input("Enter the directory containing videos to split: ").strip()
    if not os.path.isdir(input_dir):
        print(f"The directory '{input_dir}' does not exist.")
        return
    input_dir = os.path.abspath(input_dir)

    # 2. Find valid video files.
    valid_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')
    video_files = [f for f in os.listdir(input_dir)
                   if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith(valid_extensions)]
    if not video_files:
        print("No valid video files found in the specified directory.")
        return

    # 3. Process each video file.
    for video in video_files:
        full_path = os.path.join(input_dir, video)
        duration = get_video_duration(full_path)
        if duration <= 0:
            print(f"\nCould not determine duration for {video}. Skipping.")
            continue

        print(f"\nVideo: {video}")
        print(f"Duration: {format_time(duration)} ({duration:.2f} seconds)")

        # 4. Show common split suggestions.
        suggestions = [2, 3, 4, 5, 10]
        print("Common splits:")
        for num in suggestions:
            chunk_dur = duration / num
            print(f"  {num} chunks: ~{format_time(chunk_dur)} each")

        # 5. Ask for number of chunks to split this video.
        inp = input("Enter number of chunks to split this video into (default=2): ").strip()
        if not inp:
            num_chunks = 2
        else:
            try:
                num_chunks = int(inp)
                if num_chunks <= 0:
                    print("Number of chunks must be a positive integer. Skipping this video.")
                    continue
            except ValueError:
                print("Invalid input. Skipping this video.")
                continue

        # 6. Compute segment duration.
        chunk_duration = duration / num_chunks
        print(f"Splitting {video} into {num_chunks} chunks (~{format_time(chunk_duration)} each).")

        # 7. Create an output folder for this video.
        base, ext = os.path.splitext(video)
        output_dir = os.path.join(input_dir, base + "_chunks")
        os.makedirs(output_dir, exist_ok=True)
        # Use the same base filename with a 001, 002 suffix.
        output_pattern = os.path.join(output_dir, f"{base}_%03d{ext}")

        # 8. Build the FFmpeg command using the segment muxer.
        # Note the addition of "-f segment" to instruct ffmpeg to split into segments.
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", full_path,
            "-c", "copy",
            "-map", "0",
            "-segment_time", str(chunk_duration),
            "-reset_timestamps", "1",
            "-f", "segment",
            output_pattern,
            "-y"  # Overwrite output files if they exist.
        ]
        # Append progress flags.
        progress_cmd = ffmpeg_cmd[:] + ["-progress", "pipe:1", "-nostats"]

        print("\n=== Starting splitting for", video, "with progress ===")
        print("DEBUG: Running command:")
        print(" ".join(progress_cmd))
        start_time = time.time()

        proc = subprocess.Popen(
            progress_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        processed_seconds = 0.0
        # Read progress information line by line.
        while True:
            line = proc.stdout.readline()
            if not line:
                break  # End of output.
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
            # Compute percentage progress based on the total duration.
            progress_percent = (processed_seconds / duration) * 100 if duration > 0 else 0
            if progress_percent > 100:
                progress_percent = 100
            print(f"Progress for {video}: {progress_percent:5.2f}%", end="\r")
            sys.stdout.flush()

        proc.wait()
        end_time = time.time()

        if proc.returncode != 0:
            print(f"\nSplitting {video} failed.")
            stderr_data = proc.stderr.read()
            print("=== FFmpeg stderr ===")
            print(stderr_data)
        else:
            print(f"\nFinished splitting {video} in {format_time(end_time - start_time)}.")
            print(f"Output chunks are located in: {output_dir}")

if __name__ == "__main__":
    split_videos()