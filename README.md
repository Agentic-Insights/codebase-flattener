# Directory Flattener

The Directory Flattener is a Python script that flattens a directory structure by copying files from a source directory and its subdirectories into a target directory, grouping them into folders of a specified size. It provides control over which directories and files to include in the flattening process and automatically ignores files and directories specified in the `.gitignore` file.

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
   git clone https://github.com/Agentic-Insights/context-flattener
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
    "path/to/include2"
  ]
}
```
- `include`: An array of directory or file paths to include in the flattening process. If not specified or empty, the script will not proceed with flattening unless the `--force` flag is provided.

## Additional Options
- `--tokenizer`: Specify the tokenizer to use for estimating the token count. Available options: `nltk`, `tiktoken`. If not provided, the script will use an average of both tokenizers.
- `--force`: Force flattening without a configuration file or an empty include list.

## License
This project is licensed under the [MIT License](LICENSE).