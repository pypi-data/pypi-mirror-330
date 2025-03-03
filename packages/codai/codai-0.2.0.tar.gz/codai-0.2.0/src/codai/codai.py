from codai.bot import Bot
from codai.hci import run_command, copy_to_clipboard, write_file
from codai.utils import get_codai_config, get_codai_system_str

config = get_codai_config()
model = config.get("model", "openai:gpt-4o-mini")

system = get_codai_system_str()

tools = [copy_to_clipboard, write_file, run_command]

bot = Bot(model=model, system_prompt=system, tools=tools)
