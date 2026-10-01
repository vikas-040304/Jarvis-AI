"""
smart_chat.py
Fallback handler - when Jarvis doesn't recognize a command as a specific action
(open app, spotify, vlc, system, whatsapp), it asks Google Gemini to answer like
a general-purpose assistant.

Uses Google's official google-genai SDK (not raw REST calls) - this is the
reliable way to call Gemini, and handles newer API key formats correctly.

Get a free API key (no credit card needed):
    1. Go to https://aistudio.google.com/app/apikey
    2. Sign in with a Google account
    3. Click "Create API key"
    4. Paste it into GEMINI_API_KEY in config.py
"""

from config import GEMINI_API_KEY

SYSTEM_PROMPT = (
    "You are Jarvis, a concise voice assistant. Answer in 1-3 short sentences "
    "since your answer will be read out loud."
)

MODEL = "gemini-3.6-flash"

_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def ask_gemini(question: str) -> str:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        return "I don't have a Gemini API key set up yet. Add one to config.py to enable smart chat."

    try:
        from google.genai import types

        client = _get_client()
        response = client.models.generate_content(
            model=MODEL,
            contents=question,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        return response.text.strip() if response.text else "I couldn't come up with an answer for that."

    except ImportError:
        return "The google-genai library isn't installed. Run: pip install google-genai"
    except Exception as e:
        return f"Couldn't reach Gemini: {e}"


# Keep the old function name working too, so command_router.py doesn't need changes
def ask_claude(question: str) -> str:
    return ask_gemini(question)
