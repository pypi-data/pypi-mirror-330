import os
import re
from pathlib import Path

def get_base_name(filename: str) -> str:
    """
    Extract base name from filename, handling various patterns.
    Examples:
    - "test.mp4" -> "test"
    - "test copy.mp4" -> "test"
    - "test-2.mp4" -> "test"
    """
    # Remove the extension first
    name_without_ext = os.path.splitext(filename)[0]
    
    # List of common suffixes to remove
    suffixes = [
        r'\s+copy$',           # "test copy"
        r'\s*-\s*\d+$',       # "test-2" or "test - 2"
        r'\s*\(\d+\)$',       # "test (2)"
        r'\s*\[\d+\]$',       # "test [2]"
        r'\s*\d+$'            # "test 2"
    ]
    
    # Remove each type of suffix
    base_name = name_without_ext
    for suffix in suffixes:
        base_name = re.sub(suffix, '', base_name, flags=re.IGNORECASE)
    
    return base_name.strip()

def find_and_rename_pairs(directory):
    # Convert directory to Path object for easier handling
    dir_path = Path(directory)
    
    # Dictionary to store pairs of files
    file_pairs = {}
    
    # First pass: group the files by their base names
    for file_path in dir_path.glob('*.mp4'):
        base_name = get_base_name(file_path.name)
        
        if base_name not in file_pairs:
            file_pairs[base_name] = []
        file_pairs[base_name].append(file_path)
    
    # Second pass: rename pairs
    for base_name, files in file_pairs.items():
        if len(files) == 2:  # Only process if we have a pair
            # Get file sizes
            sizes = [(f, f.stat().st_size) for f in files]
            # Sort by size
            sizes.sort(key=lambda x: x[1])
            
            # Smaller file gets A, larger gets B
            smaller_file, larger_file = sizes[0][0], sizes[1][0]
            
            # Create new names
            new_name_a = f"{base_name} A.mp4"
            new_name_b = f"{base_name} B.mp4"
            
            # Skip if files are already named correctly
            if smaller_file.name == new_name_a and larger_file.name == new_name_b:
                print(f"Skipping already correctly named pair: {base_name}")
                continue
            
            # Check if target files already exist
            if (dir_path / new_name_a).exists() or (dir_path / new_name_b).exists():
                print(f"Warning: Target names already exist for {base_name}, skipping")
                continue
            
            # Rename files
            try:
                smaller_file.rename(dir_path / new_name_a)
                larger_file.rename(dir_path / new_name_b)
                print(f"Successfully renamed pair:")
                print(f"  {smaller_file.name} -> {new_name_a}")
                print(f"  {larger_file.name} -> {new_name_b}")
            except Exception as e:
                print(f"Error renaming files for {base_name}: {e}")
        else:
            print(f"Warning: Found {len(files)} file(s) for base name '{base_name}'. Expected 2 files.")
            for f in files:
                print(f"  - {f.name}")

def rename_videos():
    # Get directory path from user
    directory = input("Enter the directory path: ").strip()
    
    # Check if directory exists
    if not os.path.isdir(directory):
        print("Error: Directory does not exist!")
        return
    
    # Process the files
    print(f"\nProcessing files in: {directory}")
    find_and_rename_pairs(directory)
    print("\nProcessing complete!")

if __name__ == "__main__":
    rename_videos()