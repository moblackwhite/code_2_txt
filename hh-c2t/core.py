import os
from filter import FileFilter

def collect_from_directory(root_dir, file_filter):
    """
    Collect content of files in a local directory and its subdirectories.

    Args:
        root_dir: Path to the directory.
        file_filter: FileFilter instance for filtering files.

    Returns:
        String containing formatted content of all matching files.
    """
    if not os.path.isdir(root_dir):
        raise ValueError(f"Error: '{root_dir}' is not a valid directory")

    result = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_dir)
            if file_filter.should_include(rel_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    file_output = f"```{rel_path}\n{content}\n```\n\n"
                    result.append(file_output)
                except Exception as e:
                    result.append(f"```{rel_path}\nError reading file: {str(e)}\n```\n\n")
    return "".join(result)
