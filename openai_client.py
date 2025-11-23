# openai_client.py
import os
from openai import OpenAI

# --- FAIL FAST ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Please export it in your environment.\n"
        "Example (Linux/macOS): export OPENAI_API_KEY='sk-xxxx'\n"
        "Example (Windows CMD): set OPENAI_API_KEY=sk-xxxx"
    )

# Allow overriding model from env
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Central OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def llm_chat(prompt: str, model: str = None, max_tokens: int = 800):
    """
    Generic helper for chat-based completion.
    Safely wraps OpenAI Responses API.
    """
    _model = model or OPENAI_MODEL

    resp = client.responses.create(
        model=_model,
        input=prompt,
        max_output_tokens=max_tokens,
        temperature=0.0,
    )

    # Extract clean text
    return resp.output_text
