def now():
    from datetime import UTC, datetime

    return datetime.now(UTC)


def generate_uuid() -> str:
    import uuid

    return str(uuid.uuid4())


def get_codai_dir() -> str:
    import os

    dirpath = os.path.join(os.path.expanduser("~"), ".codai")

    os.makedirs(dirpath, exist_ok=True)

    return dirpath


def get_codai_config() -> dict:
    import os
    import tomllib

    filepath = os.path.join(get_codai_dir(), "config.toml")

    if not os.path.exists(filepath):
        return {}

    with open(filepath, "rb") as f:
        config = tomllib.load(f)

    return config


def get_codai_system_str() -> str:
    import os

    filepath = os.path.join(get_codai_dir(), "system.md")

    if not os.path.exists(filepath):
        return ""

    with open(filepath, "r") as f:
        return f.read()


def load_codai_dotenv():
    import os
    from dotenv import load_dotenv

    load_dotenv(os.path.join(get_codai_dir(), ".env"))


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def dedent_and_unwrap(text: str) -> str:
    import textwrap

    dedented = textwrap.dedent(text.strip())

    paragraphs = dedented.split("\n\n")
    unwrapped_paragraphs = [textwrap.fill(p.replace("\n", " ")) for p in paragraphs]

    result = "\n\n".join(unwrapped_paragraphs)

    return result
