from codai.bot import Bot
from codai.lms import gpt_4o_mini, claude_37_sonnet, claude_35_sonnet, gemini_2_flash  # noqa
from codai.utils import dedent_and_unwrap

system = """
You are codai -- Cody, but AI.
You are Cody's digital twin.
You are professional, highly technical, precise, and concise.
"""
system = dedent_and_unwrap(system)

bot = Bot(model=gpt_4o_mini, system_prompt=system)
