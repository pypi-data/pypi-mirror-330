from codai.bot import Bot
from codai.lms import gpt_4o

from codai.filesystem import choose_relevant_files, files_to_str, write_file

system = """
# fileystem

You are a filesystem bot. You typically:

- choose relevant files, resulting in a list of files
- convert the list of files to a string, resulting in a string with all the contents
- write the string to a file, resulting in a file with the contents
"""

tools = [choose_relevant_files, files_to_str, write_file]

bot = Bot(name="filesystem", system_prompt=system, model=gpt_4o, tools=tools)
