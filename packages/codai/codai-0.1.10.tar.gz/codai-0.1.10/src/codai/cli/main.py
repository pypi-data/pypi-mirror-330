# imports
import os
import typer
import subprocess

from codai.repl import print
from codai.utils import get_codai_dir
from codai.cli.common import default_kwargs

from codai.cli.chat import chat_app, interactive
from codai.cli.todo import todo_app

# typer config
## main app
app = typer.Typer(help="codai", **default_kwargs)

## sub-apps
app.add_typer(chat_app, name="dev")
app.add_typer(chat_app, name="chat", hidden=True)
app.add_typer(todo_app, name="todo")


# commands
@app.callback(invoke_without_command=True)
def default():
    interactive()


@app.command()
@app.command("c", hidden=True)
def config(
    vim: bool = typer.Option(False, "--vim", "-v", help="open with (n)vim"),
    env: bool = typer.Option(False, "--env", "-e", help="configure the .env file"),
    system: bool = typer.Option(False, "--system", "-s", help="configure the system"),
):
    """
    open config file
    """

    program = "vim" if vim else "nvim"
    # filename = ".env" if env else "config.toml"

    if sum([env, system]) > 1:
        print("only one option can be selected")
        return

    if env:
        filename = ".env"
    elif system:
        filename = "system.md"
    else:
        filename = "config.toml"

    filename = os.path.join(get_codai_dir(), filename)

    print(f"opening {filename} with {program}...")
    subprocess.call([program, f"{filename}"])
