import click
from pathlib import Path
from shutil import which
from . import generate as generate_module
from . import rename as rename_module
from . import combine as combine_module
from . import compress as compress_module
from . import audio as audio_module
from . import connect as connect_module

def ensure_ffmpeg_installed():
    """Check if ffmpeg is installed and accessible, and display its path."""
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path is None:
        click.echo("Error: ffmpeg is not installed or not found in your system PATH.", err=True)
        click.echo("Please install ffmpeg before using this tool. Visit https://ffmpeg.org/download.html for instructions.")
        exit(1)
    click.echo(f"ffmpeg is installed and found at: {ffmpeg_path}")

@click.group()
def main():
    """Video utility tools for combining and managing video files."""
    ensure_ffmpeg_installed()

@main.command()
def rename():
    """Rename video pairs in a directory."""
    rename_module.rename_videos()

@main.command()
def generate():
    """Generate test video pairs."""
    generate_module.generate_videos()

@main.command()
def combine():
    """Combine video pairs in a directory."""
    combine_module.combine_videos()

@main.command()
def compress():
    """Compress video pairs in a directory."""
    compress_module.compress_videos()


@main.command()
def audio():
    """Adjust volume and frequency"""
    audio_module.adjust_audio()


@main.command()
def connect():
    """Connect videos in a directory by numeric order or file creation time."""
    connect_module.connect_videos()

if __name__ == '__main__':
    main()