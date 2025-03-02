import os
import re
import time
import subprocess
import tempfile
import sys

def format_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

def parse_numeric_in_filename(filename):
    """
    Try to find a numeric pattern in the filename (e.g. 'MOVI0001.avi', 'Video (2).mp4').
    Return an integer if found, or None if no suitable pattern is detected.
    """
    # Look for groups of digits anywhere in the filename
    matches = re.findall(r'(\d+)', filename)
    if not matches:
        return None
    # Heuristic: take the last match if multiple numeric groups are present
    # for example "Video (2).mp4" -> ["2"]
    # or "MOVI0010.avi" -> ["0010"]
    # We'll interpret that as an integer
    numeric_str = matches[-1]
    try:
        return int(numeric_str)
    except ValueError:
        return None
    

def get_video_duration(video_path):
    """
    Use ffprobe to get the duration (in seconds) of a single video file.
    Returns a float. If it fails, returns 0.0.
    """
    cmd = [
        'ffprobe', '-v', 'error',
        '-of', 'csv=p=0',
        '-show_entries', 'format=duration',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return 0.0
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0

def connect_videos():
    # 1. Ask for the input directory
    input_dir = input("Enter the directory containing videos to combine and compress: ").strip()
    input_dir = os.path.abspath(input_dir)  # <--- Force absolute path
    if not os.path.isdir(input_dir):
        print(f"The directory '{input_dir}' does not exist.")
        return

    # 2. Ask for resolution shrink percentage
    resolution = input("Enter resolution shrinking percentage (high=100, mid=75, low=50, default: high): ").strip().lower() or 'high'
    resolution_map = {'high': 1.0, 'mid': 0.75, 'low': 0.5}
    if resolution not in resolution_map:
        print(f"Invalid resolution setting '{resolution}', using 'high'")
        resolution = 'high'
    scaling_factor = resolution_map[resolution]

    # 3. Ask for quality (crf)
    quality = input("Enter quality (high/mid/low, default: mid): ").strip().lower() or 'mid'
    settings = {
        'high': {'preset': 'slower', 'crf': 18},
        'mid':  {'preset': 'medium', 'crf': 23},
        'low':  {'preset': 'faster', 'crf': 28},
    }
    if quality not in settings:
        print(f"Invalid quality setting '{quality}', using 'mid'")
        quality = 'mid'
    preset = settings[quality]['preset']
    crf = settings[quality]['crf']

    # 4. Gather all video files
    valid_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')
    videos = []
    for fname in os.listdir(input_dir):
        fpath = os.path.join(input_dir, fname)
        if os.path.isfile(fpath) and fname.lower().endswith(valid_extensions):
            # Store the file name, numeric pattern, creation time
            numeric_val = parse_numeric_in_filename(fname)
            ctime = os.path.getctime(fpath)
            videos.append((fname, numeric_val, ctime))

    if not videos:
        print("No valid video files found in the specified directory.")
        return

    # 5. Determine if we can sort by numeric pattern or fallback to creation time
    #    If *all* files have a valid numeric pattern, sort by that numeric pattern.
    #    Otherwise, sort by creation time.
    all_have_numeric = all(v[1] is not None for v in videos)
    if all_have_numeric:
        # Sort by numeric pattern ascending
        videos.sort(key=lambda x: x[1])
        print("Sorting by numeric pattern in filenames.")
    else:
        # Sort by creation time ascending
        videos.sort(key=lambda x: x[2])
        print("Sorting by file creation time.")

    # 6. Create a temporary file that lists all videos in correct order for ffmpeg concat
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tf:
        concat_list_path = tf.name
        for fname, _, _ in videos:
            full_path = os.path.join(input_dir, fname)
            # We must quote the path in case of spaces or special chars
            tf.write(f"file '{full_path}'\n")

    # 7. Create output folder named "<input_dir>_output"
    #    Strip any trailing slash, then add "_output"
    output_dir = input_dir.rstrip('/') + "_output"
    os.makedirs(output_dir, exist_ok=True)

    # 8. Prepare the final output file in the output folder
    output_filename = "output.mp4"
    output_path = os.path.join(output_dir, output_filename)

    # 9. Calculate total input size
    total_input_size = sum(
        os.path.getsize(os.path.join(input_dir, v[0])) for v in videos
    )
    total_duration = 0.0
    for fname, _, _ in videos:
        full_path = os.path.join(input_dir, fname)
        total_duration += get_video_duration(full_path)

    # 10. Build FFmpeg command to concatenate & compress in one pass
    scale_filter = f"scale=iw*{scaling_factor}:ih*{scaling_factor}"
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-vf", scale_filter,
        "-c:v", "libx265",
        "-preset", preset,
        "-crf", str(crf),
        "-c:a", "aac",
        "-y",  # Overwrite output if exists
        output_path
    ]

    # We'll insert the progress arguments at the end
    # pipe:1 means "send progress info to stdout"
    # -nostats prevents normal ffmpeg stats from interfering.
    progress_cmd = ffmpeg_cmd[:]
    progress_cmd.insert(1, "-hide_banner")  # optional, to hide banner
    progress_cmd += ["-progress", "pipe:1", "-nostats"]

    print("\n=== Starting concatenation and compression with progress ===")
    start_time = time.time()

    # 12. Spawn FFmpeg using Popen so we can read the progress lines in real time
    proc = subprocess.Popen(
        progress_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    # We'll track out_time in seconds
    processed_seconds = 0.0

    while True:
        line = proc.stdout.readline()
        if not line:
            # No more output from FFmpeg. Could be end of process or closed stream.
            break
        
        line = line.strip()

        # FFmpeg -progress lines of interest often look like:
        # out_time_ms=123456
        # out_time=00:02:03.45
        # Or finished=1 when done.

        if line.startswith("out_time_ms="):
            # Format: out_time_ms=xxxxxx (in milliseconds)
            ms_str = line.split('=')[1]
            try:
                ms = float(ms_str)
                processed_seconds = ms / 1000000.0
            except ValueError:
                pass
        elif line.startswith("out_time="):
            # Format: out_time=hh:mm:ss.microseconds
            time_str = line.split('=')[1].strip()
            # We'll parse it into seconds with a helper
            processed_seconds = parse_hhmmss(time_str)
        
        # We can compute a percentage:
        if total_duration > 0:
            progress_percent = (processed_seconds / total_duration) * 100
            if progress_percent > 100:
                progress_percent = 100
            # Print in-place:
            print(f"Progress: {progress_percent:5.2f}%", end='\r')
            sys.stdout.flush()

    # Wait for ffmpeg to actually exit
    proc.wait()
    end_time = time.time()

    # 13. Remove the temporary concat list
    if os.path.exists(concat_list_path):
        os.remove(concat_list_path)

    # Check if ffmpeg succeeded
    if proc.returncode != 0:
        print("\nFFmpeg failed or was interrupted.")
        # If you want to see errors:
        stderr_data = proc.stderr.read()
        print("=== FFmpeg stderr ===")
        print(stderr_data)
        return

    # 14. Confirm output file exists
    if not os.path.exists(output_path):
        print("\nOutput file not found; something went wrong.")
        return

    # 15. Gather final stats
    total_output_size = os.path.getsize(output_path)
    total_time = end_time - start_time

    print("\n=== Process Complete ===")
    print(f"Total processing time: {format_time(total_time)}")
    print(f"Number of input videos: {len(videos)}")
    print(f"Total input size: {format_size(total_input_size)}")
    print(f"Output file size: {format_size(total_output_size)}")
    if total_output_size > 0:
        ratio = total_input_size / total_output_size
        print(f"Overall compression ratio: {ratio:.2f}x")
    else:
        print("Overall compression ratio: N/A (output size is 0)")
    space_saved = total_input_size - total_output_size
    if space_saved > 0:
        print(f"Space saved: {format_size(space_saved)}")
    print(f"\nOutput file created at: {output_path}")

def parse_hhmmss(timestr):
    """
    Parse an 'hh:mm:ss.xxx' string into floating seconds.
    E.g. '00:02:03.45' -> 123.45
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