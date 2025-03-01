# functions
def run_repl():
    # imports
    import ibis
    import rich
    import subprocess

    from codai.console import (
        print,
        clear,
        get_input,
        get_file_history,
    )
    from codai.bots.codai import bot

    # config
    ibis.options.interactive = True
    ibis.options.repr.interactive.max_rows = 40
    ibis.options.repr.interactive.max_depth = 8
    ibis.options.repr.interactive.max_columns = None

    # history
    history = get_file_history()

    # exit commands
    exit_commands = ["exit", "quit", "q"]
    exit_commands = [f"/{cmd}" for cmd in exit_commands]

    shell_history = ""
    while True:
        try:
            # user_input = typer.prompt("dev").strip()
            user_input = get_input("> ", history)
            if user_input.startswith("!"):
                shell_history += f"$ {user_input[1:]}"
                res = subprocess.run(user_input[1:], shell=True, capture_output=True)
                stdout = res.stdout.decode("utf-8")
                stderr = res.stderr.decode("utf-8")
                if stdout and not stderr:
                    rich.print(stdout)
                    shell_history += f"\n{stdout}"
                elif stderr and not stdout:
                    rich.print(stderr)
                    shell_history += f"\n{stderr}"
                elif stdout and stderr:
                    rich.print(stdout)
                    rich.print(stderr)
                    shell_history += f"\n{stdout}\n{stderr}"
                continue
            if user_input.startswith("/"):
                if user_input in exit_commands:
                    break
                command = user_input[1:]
                match command:
                    case "clear":
                        clear()
                        continue
                    case "clear messages":
                        bot.clear_messages()
                        continue
                    case "messages":
                        messages = bot.get_messages(bot_id=bot.id)
                        rich.print(messages)
                        continue
                    case "shell history":
                        rich.print(shell_history)
                        continue
                    case "copy":
                        message = "copy that to my clipboard"
                        bot(message)
                        continue
                    case _:
                        print(f"Unknown command: {command}")
                        continue

            # print(f"{user_input}", header="user")
            if shell_history:
                user_input = (
                    f"I have ran in my shell:\n\n{shell_history}\n\n{user_input}"
                )
                shell_history = ""
            response = bot(user_input)
            print(f"{response.data}")
            # copy_to_clipboard(response.data)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            print(f"{e}")
            break
