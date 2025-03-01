# functions
def run_repl():
    # imports
    from codai.console import print, copy_to_clipboard, get_input, get_file_history
    from codai.bots.chat import bot as chat_bot

    # history
    history = get_file_history()

    # exit commands
    exit_commands = ["exit", "quit", "q"]
    exit_commands = [f"/{cmd}" for cmd in exit_commands]

    while True:
        try:
            # user_input = typer.prompt("dev").strip()
            user_input = get_input("> ", history)
            if user_input in exit_commands:
                break
            print(f"{user_input}", header="user")
            response = chat_bot(user_input)
            print(f"{response.data}")
            copy_to_clipboard(response.data)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            print(f"{e}")
            break
