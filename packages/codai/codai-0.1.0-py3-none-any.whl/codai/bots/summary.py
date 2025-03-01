from codai.bot import Bot
from codai.lms import gemini_2_flash_lite
from codai.models import TextSummary

bot = Bot(model=gemini_2_flash_lite, result_type=TextSummary)
