from difflib import unified_diff


def git_diff(old_text: str, new_text: str) -> str:
    """Compute the diff between old and new text.
    This outputs the diff in a format similar to `git diff`.

    Args:
        old_text (str): The original text.
        new_text (str): The modified text.

    Returns:
        str: A string containing the diff output.
    """
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    diff = unified_diff(old_lines, new_lines, lineterm="")

    return "\n".join(diff)
