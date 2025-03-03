# Python File Collector

A versatile Python tool that collects and formats the content of Python files from various sources including local directories, Git repositories, and remote SSH servers.

## Features

- **Multiple Source Types**:
  - Local directories
  - Git repositories (via HTTPS or SSH URLs)
  - Remote SSH servers (using password or key-based authentication)

- **Formatted Output**:
  - Preserves directory structure
  - Each file is wrapped in Markdown code blocks
  - Relative paths are included for clarity

- **Authentication Methods**:
  - SSH key-based authentication
  - Password authentication
  - Interactive password prompt

## Requirements

- Python 3.6+
- Required packages:
  ```
  paramiko
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/python-file-collector.git
   cd python-file-collector
   ```

2. Install required dependencies:
   ```bash
   pip install paramiko
   pip install pyperclip
   ```

## Usage

### Basic Command Format

```bash
python collect_py_files.py <source> [ssh_path] [--password PASSWORD]
```

Where:
- `source`: Local directory, Git URL, or SSH address (username@hostname)
- `ssh_path`: Required only when source is an SSH address
- `--password`: Optional SSH password (will prompt if needed and not provided)

### Examples

1. **Collect from Local Directory**:
   ```bash
   python collect_py_files.py /path/to/your/directory
   ```

2. **Collect from Git Repository**:
   ```bash
   python collect_py_files.py https://github.com/username/repository
   ```
   
   Or with SSH:
   ```bash
   python collect_py_files.py git@github.com:username/repository.git
   ```

3. **Collect from SSH Server with Key Authentication**:
   ```bash
   python collect_py_files.py username@hostname /path/on/server
   ```

4. **Collect from SSH Server with Password**:
   ```bash
   python collect_py_files.py username@hostname /path/on/server --password your_password
   ```
   
   Or let it prompt for password:
   ```bash
   python collect_py_files.py username@hostname /path/on/server
   # It will prompt for password if key authentication fails
   ```

### Output Example

The output format will be:

```
```relative/path/to/file1.py
# Content of file1.py goes here
```

```relative/path/to/file2.py
# Content of file2.py goes here
```
```

## Programmatic Usage

You can also use the main function in your own Python scripts:

```python
from collect_py_files import collect_py_files_content

# Local directory
content = collect_py_files_content('/path/to/directory')

# Git repository
content = collect_py_files_content('https://github.com/username/repository')

# SSH with password
content = collect_py_files_content('username@hostname', '/path/on/server', 'password')

# Do something with the content
print(content)
```

## Error Handling

- Invalid directories will raise a `ValueError`
- SSH connection issues will be caught and reported
- File reading errors will be included in the output with error messages

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request