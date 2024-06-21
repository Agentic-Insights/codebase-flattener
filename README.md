# Codebase Flattener

The Codebase Flattener is a Python script that flattens a directory structure by copying files from a source directory and its subdirectories into a target directory, grouping them into folders of a specified size. It provides control over which directories and files to include in the flattening process and automatically ignores files and directories specified in the `.gitignore` file.

## Features
- Recursively traverses a source directory and its subdirectories.
- Copies files to a target directory, grouping them into folders of a specified size.
- Flattens the directory structure by replacing path separators with double dashes (`--`).
- Allows specifying an include list of directories and files to flatten via a JSON configuration file.
- Automatically ignores files and directories specified in the `.gitignore` file.
- Estimates token counts using NLTK and TikToken tokenizers.
- Provides user feedback and error handling.

## Requirements
- Python 3.6 or higher
- NLTK library
- TikToken library

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Agentic-Insights/codebase-flattener
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Create a `flatten-config.json` file in the source directory with the following format:
   ```json
   {
     "include": [
       "path/to/include1",
       "path/to/include2"
     ]
   }
   ```
   Replace `path/to/include1` and `path/to/include2` with the paths of directories or files you want to include in the flattening process.

2. Run the script:
   ```
   python flatten.py path/to/source/directory --target_dir path/to/target/directory
   ```
   - Replace `path/to/source/directory` with the path to the directory you want to flatten.
   - Optionally, specify the target directory using the `--target_dir` flag. If not provided, the script will create a directory named `{source_directory}_flat` in the current directory.

3. The script will flatten the specified directory structure, copying files to the target directory in separate folders based on the specified number of files per folder (default is 100).

4. If the `flatten-config.json` file is not found or the include list is empty, the script will not proceed with flattening unless the `--force` flag is provided.

## Configuration
The script allows for configuration through the `flatten-config.json` file placed in the source directory. The JSON file should have the following structure:
```json
{
  "include": [
    "path/to/include1",
    "path/to/include2",
    "path/to/directory/*",
    "**/*.txt"
  ]
}
```
- `include`: An array of file paths, directory paths, or patterns to include in the flattening process. If not specified or empty, the script will not proceed with flattening unless the `--force` flag is provided.

The `include` array supports the following types of entries:
- File paths: Specify the relative path to a specific file to include it in the flattening process. For example, `"path/to/file.txt"`.
- Directory paths: Specify the relative path to a directory to include all its files and subdirectories in the flattening process. For example, `"path/to/directory"`.
- Glob patterns: Use wildcard characters to match multiple files or directories. For example, `"path/to/directory/*"` will include all files in the specified directory, and `"**/*.txt"` will include all files with a `.txt` extension in any directory.

The script interprets the entries in the `include` array similarly to the patterns used in `.gitignore` files. It supports the following wildcard characters:
- `*`: Matches any number of characters except path separators (/ or \).
- `**`: Matches any number of characters, including path separators, to match files in nested directories.
- `?`: Matches any single character.
- `[abc]`: Matches any single character within the specified set (in this case, a, b, or c).
- `[!abc]`: Matches any single character not within the specified set.

Note that the script automatically ignores files and directories specified in the `.gitignore` file, so there is no need to duplicate those entries in the `flatten-config.json` file.

Examples of valid `include` entries:
```json
{
  "include": [
    "src/main.py",
    "src/utils",
    "tests/*.py",
    "docs/**/*.md"
  ]
}
```
- `"src/main.py"`: Includes the specific file `main.py` in the `src` directory.
- `"src/utils"`: Includes all files and subdirectories in the `src/utils` directory.
- `"tests/*.py"`: Includes all files with a `.py` extension in the `tests` directory.
- `"docs/**/*.md"`: Includes all files with a `.md` extension in the `docs` directory and its subdirectories.


## Additional Options
- `--tokenizer`: Specify the tokenizer to use for estimating the token count. Available options: `nltk`, `tiktoken`. If not provided, the script will use an average of both tokenizers.
- `--force`: Force flattening without a configuration file or an empty include list.

## License
This project is licensed under the [MIT License](LICENSE).