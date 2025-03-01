from pydantic import BaseModel, Field


class Story(BaseModel):
    title: str = Field(..., title="title", description="Title of the story.")
    text: str = Field(..., title="text", description="Text of the story.")
    moral: str = Field(..., title="moral", description="Moral of the story.")


class TextSummary(BaseModel):
    one_sentence_summary: str = Field(
        ...,
        title="one sentence summary",
        description="A one sentence summary of the text.",
    )
    one_paragraph_summary: str = Field(
        ...,
        title="one paragraph summary",
        description="A one paragraph summary of the text.",
    )
    tone: str = Field(..., title="tone", description="The tone of the text.")
    keywords: list[str] = Field(
        ..., title="keywords", description="Keywords extracted from the text."
    )
    bullet_points: list[str] = Field(
        ..., title="bullet points", description="Bullet points extracted from the text."
    )
