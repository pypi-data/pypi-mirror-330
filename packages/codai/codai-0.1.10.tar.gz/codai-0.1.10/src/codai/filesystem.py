import os
import typer
import shutil
import fnmatch

from enum import Enum
from pydantic import BaseModel

from codai.bot import Bot
from codai.lms import claude_37_sonnet, claude_35_sonnet, gemini_2_flash, gpt_4o_mini  # noqa
from codai.utils import dedent_and_unwrap


def read_file(file_path: str) -> str:
    """read file content"""
    with open(file_path, "r") as file:
        return file.read()


def write_file(file_path: str, content: str) -> str:
    """write content to file"""
    import os
    from codai.git import git_diff

    if os.path.exists(file_path):
        old_content = read_file(file_path)
    else:
        old_content = ""
    diff = git_diff(old_content, content)

    confirm = typer.confirm(f"Are you sure you want to write to {file_path}?\n\n{diff}")
    if not confirm:
        print("Aboring the write operation...")
        return "User aborted the write! Check why with them."

    with open(file_path, "w") as file:
        file.write(content)

    return "Success!"


def edit_file(file_path: str, instructions: str) -> str:
    """
    Edits a file with instructions given as context.
    """
    system = f"""
    You are editing {file_path} with the following instructions:

    {instructions}

    You will be given the old content of the file and you need to return the new content with an explanation.
    """
    system = dedent_and_unwrap(system)

    class ResultType(BaseModel):
        new_content: str
        explanation: str

    bot = Bot(
        name="edit_file",
        system_prompt=system,
        model=gpt_4o_mini,
        result_type=ResultType,
    )

    old_content = read_file(file_path)
    new_content = bot(old_content).data.new_content

    return write_file(file_path, new_content)


def copy_file(src: str, dst: str) -> None:
    shutil.copy2(src, dst)


def move_file(src: str, dst: str) -> None:
    shutil.move(src, dst)


def remove_file(file_path: str) -> None:
    os.remove(file_path)


def create_dir(dir_path: str) -> None:
    os.makedirs(dir_path, exist_ok=True)


def remove_dir(dir_path: str) -> None:
    shutil.rmtree(dir_path)


def list_dir(dir_path: str) -> list:
    return os.listdir(dir_path)


def tree(
    root: str = ".",
    max_depth: int | None = None,
    ignore_dotfiles: bool = True,
    respect_gitignore: bool = True,
    extra_ignore: list[str] = ["*.lock", "*.egg-info", ".ruff_cache"],
) -> (str, list[str]):
    root = os.path.abspath(os.path.expanduser(root))
    if not os.path.exists(root):
        raise ValueError(f"Path does not exist: {root}")

    # Initialize state
    files = []
    result = [os.path.basename(root) + "/"]
    gitignore_patterns = set()
    gitignore_patterns.update(extra_ignore)

    # Load gitignore if needed
    if respect_gitignore:
        gitignore_path = os.path.join(root, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        gitignore_patterns.add(line)

    def should_ignore(path: str, is_dir: bool = False) -> bool:
        """Check if a path should be ignored based on current settings."""
        name = os.path.basename(path)

        # Check dotfiles
        if ignore_dotfiles and name.startswith("."):
            return True

        # Check gitignore patterns
        if respect_gitignore and gitignore_patterns:
            rel_path = os.path.relpath(path, start=os.getcwd())
            for pattern in gitignore_patterns:
                if fnmatch.fnmatch(rel_path, pattern):
                    return True
                if is_dir and fnmatch.fnmatch(f"{rel_path}/*", pattern):
                    return True

        return False

    def generate_tree(path: str, prefix: str, depth: int) -> None:
        """Recursively generate tree structure."""
        if max_depth is not None and depth >= max_depth:
            return

        try:
            entries = sorted(os.scandir(path), key=lambda e: e.name.lower())
        except PermissionError:
            result.append(f"{prefix}[Permission Denied]")
            return

        # Filter entries based on ignore rules
        entries = [e for e in entries if not should_ignore(e.path, e.is_dir())]

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            marker = "└── " if is_last else "├── "

            result.append(
                f"{prefix}{marker}{entry.name}"
            ) if entry.is_file() else result.append(f"{prefix}{marker}{entry.name}/")

            if entry.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                # add a trailing slash for directories
                generate_tree(entry.path, new_prefix, depth + 1)
            elif entry.is_file():
                files.append(entry.path)

    # Generate the tree structure
    generate_tree(root, "", 0)

    return "\n".join(result), files


def files_to_str(files: list[str]) -> str:
    """Convert list of files to a markdown string"""
    file_str = "# Files\n\nThe filenames are in H2 headers with the file content below between quadruple backticks.\n\n"
    for file in files:
        # read in the content
        content = read_file(file)
        # add the filename as a header
        file_str += f"## {file}\n\n"
        # add the content
        file_str += f"````\n{content}\n````\n\n"

    return file_str


def choose_relevant_files(
    context: str, root: str = ".", max_depth: int = None
) -> list[str]:
    """Choose relevant files based on the context, given in text.

    Context must be sufficient to decide between all the files in the root directory.
    """
    system = """
    You are a filesystem function that takes in relevant context, including the tree structure of the files you have access to.

    You return a list of strings corresponding to the full paths of the list of files that are relevant to the context.

    Index on returning more relevant files than less!

    Follow directions in the context.
    """
    system = dedent_and_unwrap(system)

    tree_str, files = tree(root, max_depth=max_depth)

    context = f"context: \n\n{context}"
    context += f"\n\nYou have access to the following files:\n{tree_str}"

    # build an enum of allowed file paths
    files_enum = Enum("Files", {file: file for file in files})

    class ResultType(BaseModel):
        files: list[files_enum]

    bot = Bot(
        name="choose_relevant_files",
        system_prompt=system,
        model=gpt_4o_mini,
        result_type=ResultType,
    )

    res = bot(context)

    return [file.value for file in res.data.files]


def read_relevant_files(context: str, root: str = ".", max_depth: int = None) -> str:
    """Read relevant files based on the context, given in text.

    Context must be sufficient to decide between all the files in the root directory.
    """
    relevant_files = choose_relevant_files(context, root, max_depth)
    return files_to_str(relevant_files)
