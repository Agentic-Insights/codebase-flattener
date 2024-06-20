import argparse
import json
from pathlib import Path
from simplify_directory import flatten_directory, count_tokens

def load_config(src_dir):
    """
    Loads the configuration from the flatten-config.json file in the source directory.

    Args:
        src_dir (str or Path): The path to the source directory.

    Returns:
        dict: The loaded configuration, or an empty dictionary if the file doesn't exist.
    """
    config_path = Path(src_dir, "flatten-config.json")
    if config_path.exists():
        with open(config_path, "r") as file:
            config = json.load(file)
            include_list = config.get("include", [])
            if include_list:
                print(f"Configuration loaded from {config_path} with {len(include_list)} entries in the include list.")
            else:
                print(f"Configuration file {config_path} found, but the include list is empty.")
            return config
    else:
        print(f"No configuration file found at {config_path}.")
        return {}

def main():
    parser = argparse.ArgumentParser(description="Flatten a directory structure.")
    parser.add_argument("source_dir", help="The source directory to flatten.")
    parser.add_argument("--target_dir", help="The target directory for the flattened files.")
    parser.add_argument("--tokenizer", default=None, help="The tokenizer to use for estimating the token count. Available options: 'nltk', 'tiktoken'.")
    parser.add_argument("--force", action="store_true", help="Force flattening without a configuration file.")
    args = parser.parse_args()

    source_dir = args.source_dir
    target_dir = args.target_dir or f"{Path(source_dir).name}_flat"
    tokenizer = args.tokenizer
    force_flattening = args.force

    config = load_config(source_dir)
    include_list = config.get("include", [])

    if not include_list and not force_flattening:
        print("No configuration file found or include list is empty.")
        print("If you want to flatten the entire directory, run the script with the --force flag.")
        return

    token_counts = count_tokens(source_dir, include_list, tokenizer)
    estimated_tokens, nltk_tokens, tiktoken_tokens = token_counts

    print(f"Estimated token count (using '{tokenizer or 'average'}' tokenizer): {estimated_tokens:,}")
    print(f"NLTK token count: {nltk_tokens:,}")
    print(f"TikToken token count: {tiktoken_tokens:,}")

    flatten_directory(source_dir, target_dir, include_list)

if __name__ == "__main__":
    main()