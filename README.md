# Directory Flattener

The main purpose of this is to flatten a codebase for fitting it into Gemini's token limits. Gemini Pro 1.5 is currently at 1MM with a 2MM token waitlist. It provides a way to pluck just the logical pieces out of the codebase and get around the hierarchy issues with some codebases (thus flattener).

This Python script flattens a directory structure by copying files from a source directory and its subdirectories into a target directory, grouping them into folders of a specified size. It provides control over which directories and files to include in the flattening process.

For token counting, the script uses the `nltk` library to tokenize the text using the `word_tokenize` function from the `punkt` tokenizer. It also uses the `tiktoken` library to tokenize the text using the GPT-2 encoding.


## Features
- Recursively traverses a source directory and its subdirectories.
- Copies files to a target directory, grouping them into folders of a specified size.
- Flattens the directory structure by prefixing the file names with their relative paths.
- Allows specifying an include list of directories and files to flatten via a JSON configuration file.
- Adds a custom file extension to the flattened files.
- Opens the target directory in the default file explorer after the flattening process is complete.

## Usage
1. Clone or download the repository to your local machine.
2. Install the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```
3. (Optional) Create a `flatten-config.json` file in the same directory as the script, with the following format:
   - `include`: An array of directory or file paths to include in the flattening process. If not specified or empty, the entire source directory will be flattened.
   Replace the paths with the desired directories or files to include in the flattening process.
4. Run the script from the command line:
    ```
    python main.py path/to/source/directory --target_dir path/to/target/directory
    ```
   - Replace `path/to/source/directory` with the path to the directory you want to flatten.
   - (Optional) Replace `path/to/target/directory` with the desired target directory. If not provided, the script will create a directory named `flat-<source_directory_name>` in the current directory.
5. The script will flatten the specified directory structure, copying files to the target directory in separate folders based on the specified number of files per folder (default is 100).
6. If a `flatten-config.json` file exists and contains an `include` list, only the specified directories and files will be flattened. Otherwise, the entire source directory will be flattened.
7. After the flattening process is complete, the script will open the target directory in the default file explorer.

## Configuration
The script allows for configuration through a `flatten-config.json` file. The JSON file should have the following structure:
  ```
  {
    "include": [
      "path/to/include1",
      "path/to/include2"
    ]
  }
  ```
- `include`: An array of directory or file paths to include in the flattening process. If not specified or empty, the entire source directory will be flattened.

## Customization
The script provides some customization options through constants defined in the `flatten_directory.py` file:
- `DEFAULT_FILES_PER_FOLDER`: The default number of files per folder (default is 100).
- `FLATTENED_FILE_EXTENSION`: The file extension to be added after the original extension (default is ".txt").

Feel free to modify these constants according to your requirements.

## Notes
- The script preserves the original file extensions and appends the specified extension (default is ".txt") after the original extension.
- If a file with the same name already exists in the target directory, the script will skip copying that file and print a warning message.