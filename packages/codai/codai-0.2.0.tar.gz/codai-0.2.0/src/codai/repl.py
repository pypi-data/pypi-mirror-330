# imports
import os
import glob
import ibis
import rich
import subprocess

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory, InMemoryHistory
from prompt_toolkit.completion import Completer, Completion

from codai.hci import clear, print, copy_to_clipboard
from codai.utils import get_codai_dir

from codai.codai import bot


# classes
class PathCompleter(Completer):
    def get_completions(self, document, complete_event):
        if not complete_event.completion_requested:
            return

        full_text = document.text_before_cursor
        if full_text.startswith("!"):
            parts = full_text.split(maxsplit=1)
            if len(parts) > 1:
                file_fragment = parts[1]
                start_pos = -len(file_fragment)
            else:
                file_fragment = ""
                start_pos = 0
        else:
            file_fragment = full_text
            start_pos = 0

        expanded = os.path.expanduser(file_fragment)
        matches = glob.glob(expanded + "*")
        for match in matches:
            yield Completion(match, start_position=start_pos)


# functions
def get_input(prompt_text: str, history: FileHistory | InMemoryHistory) -> str:
    session = PromptSession(history=history, completer=PathCompleter())
    return session.prompt(prompt_text)


def run_repl():
    # config
    ibis.options.interactive = True
    ibis.options.repr.interactive.max_rows = 40
    ibis.options.repr.interactive.max_depth = 8
    ibis.options.repr.interactive.max_columns = None

    # history
    history = FileHistory(os.path.join(get_codai_dir(), "bots.history"))

    # exit commands
    exit_commands = ["exit", "quit", "q"]
    exit_commands = [f"/{cmd}" for cmd in exit_commands]

    shell_history = ""
    last_response = None
    while True:
        try:
            user_input = get_input("> ", history)
            if user_input.startswith("!"):
                cmd = user_input[1:]
                shell_history += f"$ {cmd}"
                profile_file = "~/.bash_aliases"
                cmd = f". {profile_file} && {cmd}"
                res = subprocess.run(cmd, shell=True, capture_output=True)
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
                    case "copy":
                        if last_response:
                            copy_to_clipboard(last_response.data)
                        continue
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
                    case "bot":
                        rich.print(bot.get_bot(id=bot.id))
                        continue
                    case "shell history":
                        rich.print(shell_history)
                        continue
                    case "copy":
                        message = "copy that to my clipboard"
                        bot(message)
                        continue
                    case _:
                        rich.print(f"Unknown command: {command}")
                        continue

            # print(f"{user_input}", header="user")
            if shell_history:
                user_input = f"Shell:\n\n{shell_history}\n\n{user_input}"
                shell_history = ""
            response = bot(user_input)
            last_response = response
            print(f"{response.data}")
            # copy_to_clipboard(response.data)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            print(f"{e}")
            break
