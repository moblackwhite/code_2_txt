import os
import subprocess
import tempfile
import shutil
from .core import collect_from_directory
from .filter import FileFilter

def collect_from_git(git_url, file_filter):
    """
    Collect content of files from a Git repository.

    Args:
        git_url: URL of the Git repository.
        file_filter: FileFilter instance for filtering files.

    Returns:
        String containing formatted content of all matching files.
    """
    temp_dir = tempfile.mkdtemp()
    try:
        print(f"Cloning repository from {git_url} to {temp_dir}...")
        subprocess.run(['git', 'clone', git_url, temp_dir], check=True)
        return collect_from_directory(temp_dir, file_filter)
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
