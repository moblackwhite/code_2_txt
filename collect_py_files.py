import os
import sys
import subprocess
import tempfile
import paramiko
import shutil
import stat
import pyperclip
from urllib.parse import urlparse

def collect_py_files_content(source, ssh_path=None, ssh_password=None):
    """
    Collect content of all .py files from different sources:
    1. Local directory
    2. Git repository URL
    3. SSH server path

    Args:
        source: Local directory path, Git URL, or SSH username@host
        ssh_path: Remote path on SSH server (required only when source is SSH address)
        ssh_password: Password for SSH authentication (optional)

    Returns:
        String containing formatted content of all .py files
    """
    temp_dir = None
    try:
        # Case 1: Git URL
        if source.startswith(('http://', 'https://', 'git@')):
            temp_dir = tempfile.mkdtemp()
            print(f"Cloning repository from {source} to {temp_dir}...")
            subprocess.run(['git', 'clone', source, temp_dir], check=True)
            root_dir = temp_dir

        # Case 2: SSH address
        elif '@' in source and ssh_path:
            return collect_from_ssh(source, ssh_path, ssh_password)

        # Case 3: Local directory
        else:
            root_dir = source
            if not os.path.isdir(root_dir):
                raise ValueError(f"Error: '{root_dir}' is not a valid directory")

        return collect_from_directory(root_dir)

    finally:
        # Clean up temporary directory if created
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def collect_from_directory(root_dir):
    """
    Collect content of all .py files in a local directory and its subdirectories.
    """
    result = []
    # Walk through all directories and files
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter only .py files
        py_files = [f for f in filenames if f.endswith('.py')]
        for py_file in py_files:
            full_path = os.path.join(dirpath, py_file)
            # Calculate relative path from root_dir
            rel_path = os.path.relpath(full_path, root_dir)
            # Read file content
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Format as requested
                file_output = f"```{rel_path}\n{content}\n```\n\n"
                result.append(file_output)
            except Exception as e:
                result.append(f"```{rel_path}\nError reading file: {str(e)}\n```\n\n")

    # Join all file contents with the specified separator
    return "".join(result)


def collect_from_ssh(ssh_address, remote_path, password=None):
    """
    Collect content of all .py files from a remote SSH server.

    Args:
        ssh_address: SSH address in format username@hostname
        remote_path: Path on the remote server
        password: Password for SSH authentication (optional)

    Returns:
        String containing formatted content of all .py files
    """
    result = []

    # Parse SSH address
    if '@' not in ssh_address:
        raise ValueError("SSH address must be in format username@hostname")

    username, hostname = ssh_address.split('@', 1)
    port = 22  # Default SSH port

    # Check if port is specified in hostname
    if ':' in hostname:
        hostname, port_str = hostname.split(':', 1)
        port = int(port_str)

    try:
        # Establish SSH connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect with password if provided, otherwise try key-based authentication
        if password:
            client.connect(hostname, port=port, username=username, password=password)
        else:
            try:
                client.connect(hostname, port=port, username=username)
            except paramiko.ssh_exception.AuthenticationException:
                # If key-based authentication fails, prompt for password
                if not password:
                    import getpass
                    password = getpass.getpass(f"Password for {username}@{hostname}: ")
                    client.connect(hostname, port=port, username=username, password=password)

        # Create SFTP client
        sftp = client.open_sftp()

        # Helper function to recursively find .py files
        def find_py_files(sftp, path, base_path):
            files = []
            try:
                for entry in sftp.listdir_attr(path):
                    full_path = f"{path}/{entry.filename}"
                    rel_path = os.path.relpath(full_path, base_path)

                    if stat.S_ISDIR(entry.st_mode):  # Directory
                        files.extend(find_py_files(sftp, full_path, base_path))
                    elif entry.filename.endswith('.py'):
                        files.append((full_path, rel_path))
            except Exception as e:
                result.append(f"```Error listing directory {path}: {str(e)}\n```\n\n")
            return files

        # Find all Python files
        py_files = find_py_files(sftp, remote_path, remote_path)

        # Read content of each Python file
        for full_path, rel_path in py_files:
            try:
                with sftp.file(full_path, 'r') as f:
                    content = f.read().decode('utf-8')
                file_output = f"```{rel_path}\n{content}\n```\n\n"
                result.append(file_output)
            except Exception as e:
                result.append(f"```{rel_path}\nError reading file: {str(e)}\n```\n\n")

        return "".join(result)

    finally:
        # Close SSH connection
        if 'client' in locals():
            client.close()

def copy_to_clipboard(text):
    """
    将文本复制到剪贴板

    Args:
        text: 要复制到剪贴板的文本

    Returns:
        bool: 是否成功复制到剪贴板
    """
    if pyperclip is not None:
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"复制到剪贴板失败: {str(e)}")
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <source> [ssh_path] [--password PASSWORD] [--no-clipboard]")
        print("  source: local directory, git URL, or SSH address (username@hostname)")
        print("  ssh_path: required only when source is SSH address")
        print("  --password: optional SSH password (alternatively, will prompt if needed)")
        print("  --no-clipboard: disable copying result to clipboard")
        sys.exit(1)

    # Parse arguments
    source = sys.argv[1]
    ssh_path = None
    ssh_password = None
    copy_clipboard = True  # 默认复制到剪贴板

    # Check for remaining arguments
    remaining_args = sys.argv[2:]
    i = 0
    while i < len(remaining_args):
        if remaining_args[i] == "--password" and i + 1 < len(remaining_args):
            ssh_password = remaining_args[i + 1]
            # Remove password and its value from args list
            remaining_args = remaining_args[:i] + remaining_args[i + 2:]
            continue
        elif remaining_args[i] == "--no-clipboard":
            copy_clipboard = False
            # Remove --no-clipboard from args list
            remaining_args = remaining_args[:i] + remaining_args[i + 1:]
            continue
        i += 1

    # First remaining arg is ssh_path if present
    if remaining_args:
        ssh_path = remaining_args[0]

    try:
        result = collect_py_files_content(source, ssh_path, ssh_password)
        print(result)
        print(f"Total characters: {len(result)}")

        # 复制到剪贴板（仅Windows系统或设置了复制标志）
        if copy_clipboard and pyperclip is not None:
            if copy_to_clipboard(result):
                print("已成功复制结果到剪贴板！")
            else:
                print("复制到剪贴板失败！")

        # Optionally, save to a file
        # with open("py_files_content.txt", "w", encoding="utf-8") as f:
        #     f.write(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()