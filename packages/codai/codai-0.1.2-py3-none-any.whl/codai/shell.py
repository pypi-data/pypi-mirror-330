def run_command(command: str) -> str:
    """
    Run shell command and return the output
    """
    import subprocess

    res = subprocess.run(command, shell=True, capture_output=True)
    stdout = res.stdout.decode("utf-8")
    stderr = res.stderr.decode("utf-8")

    if stdout and not stderr:
        return stdout
    elif not stdout and stderr:
        return stderr
    else:
        return f"{stdout}\n\n{stderr}"
