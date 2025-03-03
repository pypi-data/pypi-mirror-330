# imports
import typer

from codai.cli.common import default_kwargs

# typer config
## dev app
dev_app = typer.Typer(help="dev", **default_kwargs)


# commands
@dev_app.callback(invoke_without_command=True)
def default():
    interactive()


@dev_app.command()
@dev_app.command("i", hidden=True)
def interactive():
    """
    interactive dev
    """
    from codai.repl import run_repl

    run_repl()
