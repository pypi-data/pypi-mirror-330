from codai.bot import Bot
from codai.lms import gpt_4o_mini, claude_37_sonnet, claude_35_sonnet, gemini_2_flash  # noqa
from codai.shell import run_command
from codai.utils import dedent_and_unwrap, get_codai_config
from codai.clipboard import copy_to_clipboard
from codai.filesystem import edit_file

system = """
You are Codai, an expert developer in a terminal.
You are professional, technical, precise, concise, and helpful.
You work with the user, with your ability to copy to their clipboard, edit files, and run shell commands.

You will see the shell commands the user runs, which they use to open files and such.

To edit a file, you must provide the filepath + all relevant context as a string into the input method. It will then adjust the content accodingly.

You MUST give final responses to the user in markdown format, with code blocks for code.
"""
system = dedent_and_unwrap(system)

tools = [copy_to_clipboard, edit_file, run_command]

config = get_codai_config()
model = config.get("model", "openai:gpt-4o-mini")

bot = Bot(model=model, system_prompt=system, tools=tools)
