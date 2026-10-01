"""
screen_reader.py
Takes a screenshot of your current screen and asks Gemini to explain what's
on it - useful for reading error messages, summarizing code, describing a
webpage, or anything else visible on screen.

Uses the same Gemini API key as smart_chat.py (GEMINI_API_KEY in config.py).
"""

import io
from config import GEMINI_API_KEY

MODEL = "gemini-3.6-flash"

_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def read_screen(question: str = "What's on my screen? Explain it concisely, in 2-3 sentences since this will be read aloud.") -> str:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        return "I don't have a Gemini API key set up yet. Add one to config.py to enable this."

    try:
        from PIL import ImageGrab
        from google.genai import types
    except ImportError as e:
        return f"A required library isn't installed: {e}"

    try:
        img = ImageGrab.grab()
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()

        client = _get_client()
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
                question,
            ],
        )
        return response.text.strip() if response.text else "I looked at the screen but couldn't describe it clearly."

    except Exception as e:
        return f"Couldn't read the screen: {e}"
