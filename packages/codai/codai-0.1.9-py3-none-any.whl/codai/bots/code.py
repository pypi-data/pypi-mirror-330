from pydantic import BaseModel, Field

from codai.bot import Bot
from codai.lms import gpt_4o, claude_37_sonnet  # noqa

system = """
# code

You are a code bot. You are typically given the contents or one or more code files and asked to make edits. You are:

- an expert in Python, SQL, and data engineering
- follow software engineering best practices
- make small, precise, accurate edits to code files
"""


# result type
class ResultType(BaseModel):
    code: str = Field(
        ...,
        title="Code",
        description="The code after applying the change. ONLY THE CODE",
    )
    explanation: str = Field(
        ..., title="Explanation", description="Explanation of the change"
    )


bot = Bot(
    name="code", system_prompt=system, model=claude_37_sonnet, result_type=ResultType
)
