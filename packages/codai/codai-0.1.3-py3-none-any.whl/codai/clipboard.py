def copy_to_clipboard(text: str) -> str:
    """
    Copy text to clipboard
    """
    import pyperclip

    pyperclip.copy(text)

    return "Success!"
