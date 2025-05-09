# hh-c2t

**hh-c2t** is a versatile command-line tool designed to collect and format file contents from various sources, including local directories, Git repositories, and remote SSH servers. It supports customizable file filtering using a `.gitignore`-like ignore file and allows users to specify file extensions to include. The output is formatted in Markdown code blocks, making it easy to share or document, and can be copied to the clipboard for convenience.

## Features

- **Multiple Source Support**: Collect files from local directories, Git repositories, or SSH servers.
- **Flexible File Filtering**: Use a `.gitignore`-style ignore file (`hh-c2t-ignore`) to exclude unwanted files or directories.
- **Customizable Extensions**: Specify which file extensions to include (e.g., `.py`, `.txt`, `.md`).
- **Clipboard Integration**: Automatically copy the formatted output to the clipboard (optional).
- **Modular Design**: Organized into clear modules for maintainability and extensibility.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Installation

Install `hh-c2t` via pip:

```bash
pip install hh-c2t
```

### Requirements

- Python 3.9 or higher
- Dependencies (installed automatically):
  - `paramiko` (for SSH support)
  - `pyperclip` (for clipboard functionality)
- `git` (required for cloning Git repositories, must be installed separately)

## Usage

Run `hh-c2t` from the command line with the following syntax:

```bash
hh-c2t <source> [ssh_path] [options]
```

### Arguments

- `source`: The source of the files. Can be:
  - A local directory path (e.g., `/path/to/dir`)
  - A Git repository URL (e.g., `https://github.com/user/repo`)
  - An SSH address (e.g., `username@hostname`)
- `ssh_path`: The remote path on the SSH server (required only for SSH sources).

### Options

- `--password PASSWORD`: Password for SSH authentication (optional; will prompt if needed).
- `--no-clipboard`: Disable copying the output to the clipboard.
- `--ignore-file FILE`: Path to the ignore file (default: `hh-c2t-ignore`).
- `--extensions EXT`: Comma-separated list of file extensions to include (default: `.py`).

### Examples

1. **Collect Python files from a local directory**:

   ```bash
   hh-c2t /path/to/project --extensions .py
   ```

   This collects all `.py` files in `/path/to/project`, respecting the `hh-c2t-ignore` file.

2. **Collect Python and text files from a Git repository**:

   ```bash
   hh-c2t https://github.com/user/repo --extensions .py,.txt
   ```

   Clones the repository and collects `.py` and `.txt` files.

3. **Collect files from an SSH server**:

   ```bash
   hh-c2t user@host /remote/path --password mypass --extensions .py
   ```

   Connects to the SSH server and collects `.py` files from `/remote/path`.

4. **Use a custom ignore file**:

   ```bash
   hh-c2t /path/to/dir --ignore-file custom-ignore --extensions .md
   ```

   Collects `.md` files, ignoring patterns specified in `custom-ignore`.

## Ignore File

Create a file named `hh-c2t-ignore` (or specify a custom file with `--ignore-file`) to define patterns for files and directories to exclude. The syntax is similar to `.gitignore`. Example:

```
__pycache__/*
*.pyc
*.log
dist/*
build/*
*.egg-info
```

This will exclude Python cache files, logs, and build artifacts.

## Output Format

The tool outputs file contents in Markdown code blocks, with each file's relative path as the code block label.

The total character count is displayed, and the output is copied to the clipboard unless `--no-clipboard` is specified.

## Project Structure

The `hh-c2t` package is organized into modular components:

- `core.py`: Handles file collection from local directories.
- `git_handler.py`: Manages cloning and collecting from Git repositories.
- `ssh_handler.py`: Collects files from remote SSH servers.
- `filter.py`: Implements `.gitignore`-like file filtering.
- `clipboard.py`: Handles clipboard operations.
- `cli.py`: Provides the command-line interface.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository on GitHub.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to your fork (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/moblackwhite/hh-c2t) or contact [Hardy Hu](mailto:1243971719@qq.com).