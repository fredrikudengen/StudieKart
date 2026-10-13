import logging
import os

import anthropic
from fastapi import HTTPException
from pydantic import ValidationError

logger = logging.getLogger(__name__)

LLM_MODEL = "claude-sonnet-5-5"
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-do-not-use-in-production")
ALGORITHM = "HS256"
_anthropic = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def extract_text(message) -> str:
    for block in message.content:
        if block.type == "text":
            return block.text
    block_types = [block.type for block in message.content]
    raise ValueError(
        f"No text block in Anthropic response (stop_reason={message.stop_reason}, blocks={block_types})"
    )


def generate_structured(prompt: str, max_tokens: int, schema):
    """Call the LLM and parse its JSON reply into `schema`, surfacing failures as a 502 instead of an uncaught 500."""
    try:
        message = _anthropic.messages.create(
            model=LLM_MODEL,
            max_tokens=max_tokens,
            thinking={"type": "between_tools"},
            messages=[{"role": "user", "content": prompt}],
        )
        raw = extract_text(message).strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return schema.model_validate_json(raw)
    except (anthropic.APIError, ValidationError, ValueError) as e:
        logger.exception("LLM call failed for schema %s", schema.__name__)
        raise HTTPException(status_code=502, detail="Kunne ikke generere innhold fra LLM. Prøv igjen.") from e
