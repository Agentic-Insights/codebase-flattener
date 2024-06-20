import argparse
import json
from pathlib import Path
from simplify_directory import flatten_directory, count_tokens

def load_config():
    """
    Loads the configuration from the flatten-config.json file.

    Returns:
        dict: The loaded configuration, or an empty dictionary if the file doesn't exist.
    """
    config_file = Path("flatten-config.json")
    if config_file.exists():
        with open(config_file, "r") as file:
            return json.load(file)
    return {}

def prompt_user(token_counts, tokenizer):
    """
    Prompts the user to confirm whether to proceed with flattening based on the estimated token count.

    Args:
        token_counts (tuple): A tuple containing (estimated_tokens, nltk_tokens, tiktoken_tokens)
        tokenizer (str): The tokenizer used for the estimate.

    Returns:
        bool: True if the user confirms to proceed, False otherwise.
    """
    estimated_tokens, nltk_tokens, tiktoken_tokens = token_counts
    print(f"Estimated token count (using '{tokenizer or 'average'}' tokenizer): {estimated_tokens:,}")
    print(f"NLTK token count: {nltk_tokens:,}")
    print(f"TikToken token count: {tiktoken_tokens:,}")

    if estimated_tokens > 1000000:
        print("Warning: The estimated token count exceeds 1 million.")
        print("Consider removing some files or directories from the include list.")

    proceed = input("Do you want to proceed with flattening? [Y/n]: ").strip().lower()
    return proceed == "" or proceed == "y"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatten a directory structure.")
    parser.add_argument("source_dir", help="The source directory to flatten.")
    parser.add_argument("--target_dir", help="The target directory for the flattened files. This is where the flattened files will be copied to, leaving the source directory unchanged.")
    parser.add_argument("--tokenizer", default=None, help="The tokenizer to use for estimating the token count. Available options: 'nltk', 'tiktoken'. If not provided, uses an average of both tokenizers.")
    args = parser.parse_args()

    source_dir = args.source_dir
    target_dir = args.target_dir or f"flat-{Path(source_dir).name}"
    tokenizer = args.tokenizer

    config = load_config()
    include_list = config.get("include", [])

    token_counts = count_tokens(source_dir, include_list, tokenizer)

    if prompt_user(token_counts, tokenizer):
        print("\nFlattening in progress...")
        flatten_directory(source_dir, target_dir, include_list)
        print(f"\nDone! The flattened files have been copied to '{target_dir}' directory, leaving the source directory unchanged.")
        print("The flattened folder will now open.")
    else:
        print("Flattening process aborted.")