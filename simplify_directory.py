import os
import shutil
from pathlib import Path
import fnmatch
import glob
import subprocess

# Constants based on Gemini UI restrictions
DEFAULT_FILES_PER_FOLDER = 100
FLATTENED_FILE_EXTENSION = ".txt"

# Token estimation constants
AVERAGE_CHARS_PER_TOKEN = 4  # A reasonable approximation for English text
WHITESPACE_MULTIPLIER = 0.8  # Adjustment factor for whitespace

def read_gitignore(src_dir):
    """
    Reads the .gitignore file in the source directory and returns a list of patterns to ignore.

    Args:
        src_dir (str or Path): The path to the source directory.

    Returns:
        list: A list of patterns to ignore based on the .gitignore file.
    """
    gitignore_path = Path(src_dir, ".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, "r") as file:
            return [line.strip() for line in file if line.strip() and not line.startswith("#")]
    return []

def should_ignore(file_path, ignore_patterns):
    """
    Determines whether a file should be ignored based on the ignore patterns.

    Args:
        file_path (str or Path): The path to the file.
        ignore_patterns (list): A list of patterns to ignore.

    Returns:
        bool: True if the file should be ignored, False otherwise.
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(str(file_path), pattern):
            return True
    return False

def should_include(file_path, include_patterns):
    """
    Determines whether a file should be included based on the include patterns.

    Args:
        file_path (str or Path): The path to the file.
        include_patterns (list): A list of glob patterns to include.

    Returns:
        bool: True if the file should be included, False otherwise.
    """
    if not include_patterns:
        return True
    file_path_str = str(file_path)
    return any(fnmatch.fnmatch(file_path_str, pattern) for pattern in include_patterns)

def flatten_directory(src_dir, dst_dir, include_list=None, files_per_folder=DEFAULT_FILES_PER_FOLDER):
    """
    Flattens a directory structure, copying files to the target directory.

    Args:
        src_dir (str or Path): The path to the source directory.
        dst_dir (str or Path): The path to the target directory.
        include_list (list, optional): A list of glob patterns to include in the flattening process.
        files_per_folder (int, optional): The maximum number of files per folder. Defaults to DEFAULT_FILES_PER_FOLDER.
    """
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)

    # Create the target directory if it doesn't exist
    dst_dir.mkdir(parents=True, exist_ok=True)

    ignore_patterns = read_gitignore(src_dir)

    files_copied = 0
    current_folder = 1
    folder_path = dst_dir / f"folder{current_folder}"
    folder_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(src_dir):
        for file in files:
            file_path = Path(root, file)
            relative_path = file_path.relative_to(src_dir)

            # Skip files specified in .gitignore
            if should_ignore(relative_path, ignore_patterns):
                continue

            # Skip files not matching include patterns
            if not should_include(relative_path, include_list):
                continue

            # Create a new folder if the current folder has reached the maximum number of files
            if files_copied % files_per_folder == 0 and files_copied > 0:
                current_folder += 1
                folder_path = dst_dir / f"folder{current_folder}"
                folder_path.mkdir(parents=True, exist_ok=True)

            flattened_name = str(relative_path).replace(os.path.sep, "--")
            dst_path = folder_path / flattened_name

            shutil.copy2(file_path, dst_path)
            files_copied += 1

    print(f"Directory flattened successfully. Flattened files copied to: {dst_dir}")
    # Open the flattened folder
    open_folder(dst_dir)
    
def estimate_tokens(content):
    """
    Estimates the number of tokens in a text using a simple character-based heuristic.
    
    Args:
        content (str): The text content to estimate tokens for.
        
    Returns:
        int: Estimated number of tokens.
    """
    # Count characters excluding whitespace
    char_count = len(''.join(content.split()))
    
    # Apply whitespace adjustment (whitespace often separates tokens)
    whitespace_count = len(content) - char_count
    adjusted_count = char_count + (whitespace_count * WHITESPACE_MULTIPLIER)
    
    # Convert to token estimate
    estimated_tokens = int(adjusted_count / AVERAGE_CHARS_PER_TOKEN)
    
    return max(1, estimated_tokens)  # Ensure at least 1 token

def count_tokens(src_dir, include_list=None):
    """
    Estimates the total number of tokens in all files within a directory and its subdirectories
    using a lightweight character-based approach.

    Args:
        src_dir (str or Path): The path to the source directory.
        include_list (list, optional): A list of glob patterns to include in the token count.

    Returns:
        int: Estimated token count for the directory.
    """
    total_tokens = 0
    src_dir = Path(src_dir)
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            file_path = Path(root, file)
            relative_path = file_path.relative_to(src_dir)

            # Skip files not matching include patterns
            if not should_include(relative_path, include_list):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    total_tokens += estimate_tokens(content)
            except UnicodeDecodeError:
                print(f"Skipping file '{file_path}' due to UnicodeDecodeError.")
                continue

    return total_tokens

def open_folder(path):
    """
    Opens the specified folder in the default file explorer.

    Args:
        path (str or Path): The path to the folder to open.
    """
    path = Path(path)
    if os.name == 'nt':  # Windows
        subprocess.Popen(f'explorer.exe "{path}"')
    elif os.name == 'posix':  # Linux/macOS
        subprocess.Popen(f'open "{path}"', shell=True)
    else:
        print(f"Cannot open folder '{path}' on this operating system.")
