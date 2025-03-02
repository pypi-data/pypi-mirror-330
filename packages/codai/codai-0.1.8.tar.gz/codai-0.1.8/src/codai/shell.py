def run_command(command: str) -> str:
    """
    Run shell command and return the output
    """
    import typer
    import subprocess

    confirm = typer.confirm(f"Run command: {command}?")
    if not confirm:
        typer.echo("Aborted.")
        return "User aborted running the command."

    res = subprocess.run(command, shell=True, capture_output=True)
    stdout = res.stdout.decode("utf-8")
    stderr = res.stderr.decode("utf-8")

    if stdout and not stderr:
        return stdout
    elif not stdout and stderr:
        return stderr
    else:
        return f"{stdout}\n\n{stderr}"
