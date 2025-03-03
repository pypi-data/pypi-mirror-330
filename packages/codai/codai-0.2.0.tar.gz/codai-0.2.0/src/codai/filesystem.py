def read_file(file_path: str) -> str:
    """read file content"""
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path: str, content: str) -> str:
    """write content to file"""
    import os

    from codai.hci import confirm
    from codai.git import git_diff

    if os.path.exists(file_path):
        old_content = read_file(file_path)
    else:
        old_content = ""
    diff = git_diff(old_content, content)

    confirmed = confirm(f"Are you sure you want to write to {file_path}?\n\n{diff}")
    if not confirmed:
        print("Aboring the write operation...")
        return "User aborted the write! Check why with them."

    with open(file_path, "w") as file:
        file.write(content)

    return "Success!"
