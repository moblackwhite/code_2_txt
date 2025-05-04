import pyperclip

def copy_to_clipboard(text):
    """
    Copy text to the clipboard.

    Args:
        text: Text to copy.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        print(f"Failed to copy to clipboard: {str(e)}")
        return False
