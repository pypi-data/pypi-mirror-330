import os
import subprocess
import click

def adjust_audio():
    """Adjust the volume and apply optional filters to all video files in a directory."""
    # Ask for input directory
    input_dir = input("Enter the directory containing video files: ").strip()
    if not os.path.isdir(input_dir):
        print(f"Error: The directory '{input_dir}' does not exist.")
        return

    # Ask for volume adjustment
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

    # Ask for audio filter options
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
    
    # Build the audio filter string
    audio_filter_string = f"volume={volume_factor}"
    if audio_filter:
        audio_filter_string += f",{audio_filter}"

    # Create output directory
    output_dir = input_dir.rstrip('/') + "_output"
    os.makedirs(output_dir, exist_ok=True)

    # Process each video file in the directory
    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        if not os.path.isfile(input_path) or not file_name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):
            continue

        output_path = os.path.join(output_dir, file_name)

        # Run FFmpeg command
        ffmpeg_cmd = [
            "ffmpeg", "-i", input_path,
            "-c:v", "copy",  # Copy video stream without re-encoding
            "-af", audio_filter_string,  # Apply audio filters
            output_path
        ]

        print(f"Processing '{file_name}'...")
        subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if os.path.exists(output_path):
            print(f"Adjusted audio saved at: {output_path}")
        else:
            print(f"Error: Failed to adjust audio for '{file_name}'.")

    print(f"\nProcessing complete. Adjusted files saved in: {output_dir}")