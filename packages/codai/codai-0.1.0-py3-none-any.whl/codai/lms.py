from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.vertexai import VertexAIModel
from pydantic_ai.models.anthropic import AnthropicModel

# openai models
gpt_4o = OpenAIModel("gpt-4o")
gpt_4o_mini = OpenAIModel("gpt-4o-mini")
o3_mini = OpenAIModel("o3-mini")

# vertexai models
gemini_2_flash = VertexAIModel("gemini-2.0-flash")
gemini_2_flash_lite = VertexAIModel("gemini-2.0-flash-lite-preview-02-05")
gcp_claude_37_sonnet = VertexAIModel("anthopic/claude-3-7-sonnet@20250219")
gcp_claude_35_sonnet = VertexAIModel("anthopic/claude-3-5-sonnet@latest")

# anthropic models
claude_35_haiku = AnthropicModel("claude-3-5-haiku-latest")
claude_35_sonnet = AnthropicModel("claude-3-5-sonnet-latest")
claude_37_sonnet = AnthropicModel("claude-3-7-sonnet-latest")
