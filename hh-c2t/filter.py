import fnmatch
import os

class FileFilter:
    def __init__(self, ignore_file=None, extensions=None):
        """
        Initialize the file filter.

        Args:
            ignore_file: Path to an ignore file (like .gitignore).
            extensions: List of file extensions to include (e.g., ['.py', '.txt']).
        """
        self.patterns = []
        self.extensions = extensions or ['.py']  # Default to .py
        if ignore_file and os.path.exists(ignore_file):
            with open(ignore_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.patterns.append(line)

    def should_include(self, filepath):
        """
        Check if a file should be included based on patterns and extensions.

        Args:
            filepath: Relative path of the file.

        Returns:
            bool: True if the file should be included, False otherwise.
        """
        # Check extension
        if not any(filepath.endswith(ext) for ext in self.extensions):
            return False

        # Check ignore patterns
        for pattern in self.patterns:
            if fnmatch.fnmatch(filepath, pattern) or fnmatch.fnmatch(filepath, f"*/{pattern}"):
                return False
        return True
