import os

import anthropic

LLM_MODEL = "claude-sonnet-5"
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-do-not-use-in-production")
ALGORITHM = "HS256"
_anthropic = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(message) -> str:
    for block in message.content:
        if block.type == "text":
            return block.text
    raise ValueError("No text block in Anthropic response")
