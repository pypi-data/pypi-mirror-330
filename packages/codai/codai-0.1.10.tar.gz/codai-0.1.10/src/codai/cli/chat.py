# imports
import typer

from codai.cli.common import other_kwargs

# typer config
## todo app
chat_app = typer.Typer(help="chat", **other_kwargs)


# commands
@chat_app.callback(invoke_without_command=True)
def default():
    interactive()


@chat_app.command()
@chat_app.command("i", hidden=True)
def interactive():
    """
    chat
    """
    from codai.repl import run_repl

    run_repl()
