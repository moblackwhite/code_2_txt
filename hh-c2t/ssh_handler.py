import paramiko
import stat
import os
from filter import FileFilter

def collect_from_ssh(ssh_address, remote_path, password=None, file_filter=None):
    """
    Collect content of files from a remote SSH server.

    Args:
        ssh_address: SSH address (username@hostname[:port]).
        remote_path: Path on the remote server.
        password: Password for SSH authentication (optional).
        file_filter: FileFilter instance for filtering files.

    Returns:
        String containing formatted content of all matching files.
    """
    if '@' not in ssh_address:
        raise ValueError("SSH address must be in format username@hostname")

    username, hostname = ssh_address.split('@', 1)
    port = 22
    if ':' in hostname:
        hostname, port_str = hostname.split(':', 1)
        port = int(port_str)

    result = []
    client = None
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if password:
            client.connect(hostname, port=port, username=username, password=password)
        else:
            try:
                client.connect(hostname, port=port, username=username)
            except paramiko.ssh_exception.AuthenticationException:
                import getpass
                password = getpass.getpass(f"Password for {username}@{hostname}: ")
                client.connect(hostname, port=port, username=username, password=password)

        sftp = client.open_sftp()

        def find_files(sftp, path, base_path):
            files = []
            try:
                for entry in sftp.listdir_attr(path):
                    full_path = f"{path}/{entry.filename}"
                    rel_path = os.path.relpath(full_path, base_path)
                    if stat.S_ISDIR(entry.st_mode):
                        files.extend(find_files(sftp, full_path, base_path))
                    elif file_filter.should_include(rel_path):
                        files.append((full_path, rel_path))
            except Exception as e:
                result.append(f"```Error listing directory {path}: {str(e)}\n```\n\n")
            return files

        py_files = find_files(sftp, remote_path, remote_path)
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
        if client:
            client.close()
