# imports
import typer

from codai.repl import print
from codai.cli.common import other_kwargs

# typer config
## todo app
todo_app = typer.Typer(help="todo", **other_kwargs)


# commands
@todo_app.callback(invoke_without_command=True)
def default():
    edit(vim=False)


@todo_app.command()
@todo_app.command("e", hidden=True)
@todo_app.command("open", hidden=True)
@todo_app.command("o", hidden=True)
def edit(
    vim: bool = typer.Option(False, "--vim", "-v", help="open with (n)vim"),
):
    """
    open config file
    """
    import os
    import subprocess

    from codai.utils import get_codai_dir
    from codai.todo.template import todo_file_template

    program = "vim" if vim else "nvim"
    filename = "todo.md"

    filename = os.path.join(get_codai_dir(), filename)

    if not os.path.exists(filename):
        print(f"creating {filename}...")
        with open(filename, "w") as f:
            f.write(todo_file_template.format(ntbd_todos="-", stbd_todos="-"))

    print(f"opening {filename} with {program}...")
    subprocess.call([program, f"{filename}"])


@todo_app.command()
@todo_app.command("a", hidden=True)
def add():
    """
    add
    """
    print("add")
