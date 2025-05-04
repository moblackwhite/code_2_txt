import argparse
from .core import collect_from_directory
from .git_handler import collect_from_git
from .ssh_handler import collect_from_ssh
from .filter import FileFilter
from .clipboard import copy_to_clipboard

def main():
    parser = argparse.ArgumentParser(
        description="hh-c2t: Collect and format file contents from various sources."
    )
    parser.add_argument("source", help="Local directory, Git URL, or SSH address (username@hostname)")
    parser.add_argument("ssh_path", nargs="?", help="Remote path for SSH source")
    parser.add_argument("--password", help="SSH password")
    parser.add_argument("--no-clipboard", action="store_true", help="Disable copying to clipboard")
    parser.add_argument("--ignore-file", default="hh-c2t-ignore", help="Path to ignore file")
    parser.add_argument("--extensions", help="Comma-separated file extensions (e.g., .py,.txt)", default=".py")
    
    args = parser.parse_args()

    extensions = [ext.strip() for ext in args.extensions.split(",")]
    file_filter = FileFilter(ignore_file=args.ignore_file, extensions=extensions)

    try:
        if args.source.startswith(('http://', 'https://', 'git@')):
            result = collect_from_git(args.source, file_filter)
        elif '@' in args.source and args.ssh_path:
            result = collect_from_ssh(args.source, args.ssh_path, args.password, file_filter)
        else:
            result = collect_from_directory(args.source, file_filter)

        print(result)
        print(f"Total characters: {len(result)}")

        if not args.no_clipboard:
            if copy_to_clipboard(result):
                print("Successfully copied to clipboard!")
            else:
                print("Failed to copy to clipboard!")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
