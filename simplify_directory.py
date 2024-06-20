import os
import shutil
from pathlib import Path
import subprocess
import nltk
from nltk.tokenize import word_tokenize
import tiktoken

# Constants based on Gemini UI restrictions
DEFAULT_FILES_PER_FOLDER = 100
FLATTENED_FILE_EXTENSION = ".txt"

def flatten_directory(src_dir, dst_dir, include_list=None, files_per_folder=DEFAULT_FILES_PER_FOLDER):
    """
    Simplifies a directory structure, grouping files into folders of a specified size.

    Args:
        src_dir (str or Path): The path to the source directory.
        dst_dir (str or Path): The path to the target directory.
        include_list (list, optional): A list of directories or files to include in the flattening process.
        files_per_folder (int, optional): The number of files per folder. Defaults to DEFAULT_FILES_PER_FOLDER.
    """
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)

    # Create the target directory if it doesn't exist
    dst_dir.mkdir(parents=True, exist_ok=True)

    files_copied = 0
    current_folder = 1

    for root, _, files in os.walk(src_dir):
        for file in files:
            src_path = Path(root, file)
            relative_path = src_path.relative_to(src_dir)

            # Skip files and directories not in the include list
            if include_list and str(relative_path.parent) not in include_list and str(relative_path) not in include_list:
                continue

            # Create a new folder if needed
            if files_copied % files_per_folder == 0:
                folder_name = f"folder{current_folder}"
                folder_path = dst_dir / folder_name
                folder_path.mkdir(parents=True, exist_ok=True)
                current_folder += 1

            # Preserve the original file extension
            flattened_name = str(relative_path.parent) + "--" + relative_path.stem + FLATTENED_FILE_EXTENSION
            flattened_name = flattened_name.replace(os.path.sep, '--')

            dst_path = folder_path / flattened_name

            if dst_path.exists():
                print(f"Warning: File '{dst_path}' already exists, skipping...")
                continue

            shutil.copy2(src_path, dst_path)
            files_copied += 1

    print(f"\n{files_copied} files copied to '{dst_dir}' in separate folders.")

    # Open the flattened folder
    open_folder(dst_dir)

def count_tokens(src_dir, include_list=None, tokenizer=None):
    """
    Counts the total number of tokens in all files within a directory and its subdirectories.

    Args:
        src_dir (str or Path): The path to the source directory.
        include_list (list, optional): A list of directories or files to include in the token count.
        tokenizer (str, optional): The tokenizer to use. Available options: "nltk", "tiktoken". If None, returns counts for both tokenizers.

    Returns:
        tuple: A tuple containing (estimated_tokens, nltk_tokens, tiktoken_tokens).
               If tokenizer is None, estimated_tokens is the average of nltk_tokens and tiktoken_tokens.
               If tokenizer is "nltk", estimated_tokens is equal to nltk_tokens.
               If tokenizer is "tiktoken", estimated_tokens is equal to tiktoken_tokens.
    """
    nltk.download('punkt')

    total_tokens_nltk = 0
    total_tokens_tiktoken = 0
    for root, _, files in os.walk(src_dir):
        for file in files:
            file_path = Path(root, file)
            relative_path = file_path.relative_to(src_dir)

            # Skip files and directories not in the include list
            if include_list and str(relative_path.parent) not in include_list and str(relative_path) not in include_list:
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    tokens_nltk = word_tokenize(content)
                    total_tokens_nltk += len(tokens_nltk)
                    encoding = tiktoken.get_encoding("gpt2")
                    tokens_tiktoken = encoding.encode(content)
                    total_tokens_tiktoken += len(tokens_tiktoken)
            except UnicodeDecodeError:
                print(f"Skipping file '{file_path}' due to UnicodeDecodeError.")
                continue

    if tokenizer is None:
        average_tokens = (total_tokens_nltk + total_tokens_tiktoken) // 2
        return average_tokens, total_tokens_nltk, total_tokens_tiktoken
    elif tokenizer == "nltk":
        return total_tokens_nltk, total_tokens_nltk, total_tokens_tiktoken
    elif tokenizer == "tiktoken":
        return total_tokens_tiktoken, total_tokens_nltk, total_tokens_tiktoken
    else:
        raise ValueError(f"Invalid tokenizer: {tokenizer}")

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