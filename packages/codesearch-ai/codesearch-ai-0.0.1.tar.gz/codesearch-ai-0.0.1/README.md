# CodeSearch AI

CodeSearch AI is a powerful tool that allows you to search and interact with your codebase through a web interface.

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Web Server Locally

There are two ways to run CodeSearch AI:

### 1. Running Directly from Source

```bash
python codesearch_ai/main.py
```


This will start the web server at http://localhost:8000/codesearch and automatically open it in your default browser.

### 2. Running as an Executable

First, build the executable:

```bash
# Clean any previous builds
rm -rf build dist
# Build the executable
pyinstaller --clean codesearch_ai.spec
```

Then run the executable:

```bash
./dist/codesearch_ai
```

The web interface will be available at http://localhost:8000/codesearch

## Usage

1. Open your web browser and navigate to http://localhost:8000/codesearch
2. Select a directory to analyze through the web interface
3. Start searching and interacting with your codebase

## Command Line Interface

When running with command-line arguments, CodeSearch AI provides additional functionality:

```bash
# Show help
./dist/codesearch_ai --help

# Start with specific directories
./dist/codesearch_ai start -d /path/to/dir1 /path/to/dir2

# Ignore specific paths
./dist/codesearch_ai start -i "node_modules/*" "*.pyc"
```

## Development

To modify and rebuild the executable:

1. Make your changes to the source code
2. Update dependencies in `requirements.txt` if needed
3. Rebuild the executable using the commands in the "Running as an Executable" section

### Version Control

- The `.venv` directory (virtual environment) is excluded from version control via `.gitignore`
- Also excluded are Python cache files, build artifacts, and IDE-specific files
- When cloning the repository, you'll need to create a new virtual environment and install dependencies as described in the Installation section

## Complete Reinstallation

If you need to completely clear and reinstall CodeSearch AI, follow these steps:

1. Uninstall existing packages:
```bash
pip uninstall dir-assistant codesearch-ai -y
```

2. Remove the configuration and models:
```bash
rm -rf ~/.local/share/codesearch_ai
rm -rf ~/.local/share/dir-assistant  # If you had dir-assistant installed
```

3. Clean any previous builds:
```bash
rm -rf build dist *.egg-info
```

4. Reinstall from source:
```bash
pip install -e .
```

5. Download the required models:
```bash
codesearch-ai models download-llm
codesearch-ai models download-embed
```

## Acknowledgments

CodeSearch AI is built upon the foundations of the excellent work done in
the [dir-assistant](https://github.com/curvedinf/dir-assistant) project by Chase Adams. We deeply appreciate the
contributions made by Chase Adams, as they provided invaluable insights and inspiration for the development of this
tool.
