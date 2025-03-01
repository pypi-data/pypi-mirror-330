from codai.bot import Bot
from codai.lms import claude_37_sonnet, claude_35_sonnet, gemini_2_flash  # noqa

system = (
    "You are codai -- Cody, but AI."
    + " You are Cody's digital twin."
    + " You are professional, highly technical, precise, and concise."
)

bot = Bot(model=claude_37_sonnet, system_prompt=system)
