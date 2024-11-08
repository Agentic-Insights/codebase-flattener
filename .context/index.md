# Repository Architecture Guide

## Overview
The Gemini Flattener is a Python-based utility designed to transform complex directory structures into a flattened format while preserving file relationships through naming conventions. This tool is particularly useful for preparing codebases for large language model (LLM) analysis by converting nested directory structures into a more digestible format.

## Core Components

### 1. Entry Point (main.py)
The main.py file serves as the application's entry point, handling:
- Command-line argument parsing
- Configuration file loading (flatten-config.json)
- Orchestration of the flattening process
- Token counting initialization

### 2. Core Logic (simplify_directory.py)
This module contains the primary business logic:
- Directory traversal and flattening algorithms
- File copying and renaming operations
- Token counting implementations
- .gitignore integration
- Cross-platform folder operations

## Usage Guide

### Basic Usage
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the flattener:
   ```bash
   python main.py /path/to/source --target_dir /path/to/output
   ```

### Configuration
Create a `flatten-config.json` in your source directory:
```json
{
  "include": [
    "src/**/*.py",
    "docs/*.md"
  ]
}
```

### Command Line Options
- `source_dir`: (Required) Source directory to flatten
- `--target_dir`: Output directory (defaults to source_dir_flat)
- `--tokenizer`: Choose tokenizer ('nltk' or 'tiktoken')
- `--force`: Skip configuration validation

## Architectural Decisions

### 1. File Organization
- Files are grouped into folders of 100 by default
- Path information is preserved in filenames using double-dash (--) notation
- Original file extensions are maintained

### 2. Configuration System
- JSON-based configuration for flexibility
- Support for glob patterns
- Automatic .gitignore integration
- Optional configuration with force override

### 3. Token Counting
- Dual tokenizer support (NLTK and TikToken)
- Configurable tokenizer selection
- Average token count calculation option

### 4. Error Handling
- Graceful handling of Unicode decode errors
- Clear error messages for configuration issues
- Path validation and sanitization

## Best Practices

1. Configuration Management:
   - Always use flatten-config.json for production use
   - Document included patterns in the configuration
   - Regularly update .gitignore for proper exclusions

2. Performance Optimization:
   - Use specific include patterns to limit file scanning
   - Consider file count per folder for optimal organization
   - Monitor token counting performance on large codebases

3. Cross-Platform Compatibility:
   - Use Path objects for file operations
   - Implement platform-specific folder opening
   - Handle path separators consistently

## Implementation Notes

### File Processing Flow
1. Configuration Loading
   - Parse flatten-config.json
   - Validate include patterns
   - Load .gitignore rules

2. Directory Traversal
   - Recursive file discovery
   - Pattern matching
   - Exclusion filtering

3. File Operations
   - Path flattening
   - Metadata preservation
   - Folder organization

4. Token Analysis
   - Multiple tokenizer support
   - Error handling
   - Results aggregation

### Error Handling Strategy
- Configuration errors: Early validation and clear messages
- File operations: Graceful failure with logging
- Unicode issues: Skip problematic files with notification
- Path issues: Sanitization and validation

## Future Considerations

1. Potential Enhancements:
   - Parallel processing for large directories
   - Custom folder size configuration
   - Additional tokenizer support
   - Compression options for output

2. Maintenance Guidelines:
   - Regular dependency updates
   - Cross-platform testing
   - Documentation updates
   - Performance monitoring

## Troubleshooting

Common Issues:
1. Configuration not found
   - Ensure flatten-config.json is in source directory
   - Use --force flag to override

2. Unicode errors
   - Check file encodings
   - Use appropriate text editors
   - Consider excluding problematic files

3. Performance issues
   - Limit include patterns
   - Adjust folder size
   - Monitor system resources
