from codai.bot import Bot
from codai.lms import gemini_2_flash_lite
from codai.models import Story

system_prompt = "You are a story bot!"
bot = Bot(model=gemini_2_flash_lite, system_prompt=system_prompt, result_type=Story)
