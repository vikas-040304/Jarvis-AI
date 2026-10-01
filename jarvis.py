"""
jarvis.py
This is the main Jarvis file. Run it with:
    python jarvis.py

Voice mode: say "Jarvis" (or "Hey Jarvis") followed by your command
Text mode:  type your command directly (no wake word needed)

You can also skip the mode prompt: python jarvis.py voice / python jarvis.py text
"""

import sys
import datetime

import speech_recognition as sr
import pyttsx3

from command_router import handle_command
from config import ASSISTANT_NAME, TTS_RATE, TTS_VOLUME, USE_VOICE_INPUT_BY_DEFAULT

WAKE_WORDS = ["hey jarvis", "jarvis"]

# ---------------- TTS SETUP ----------------
engine = pyttsx3.init()
engine.setProperty("rate", TTS_RATE)
engine.setProperty("volume", TTS_VOLUME)

# Pick a male voice (Windows ships with "David" - male, "Zira" - female by default)
for voice in engine.getProperty("voices"):
    if "david" in voice.name.lower() or "male" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break


def speak(text: str):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()


# ---------------- VOICE INPUT ----------------
recognizer = sr.Recognizer()


def listen() -> str:
    """Listens through the mic and converts speech to English text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        speak(f"Speech recognition service problem: {e}")
        return ""


def strip_wake_word(text: str):
    """
    Returns the command with the wake word removed, or None if no wake word
    was found anywhere in the sentence.
    """
    lower = text.lower()
    for wake in sorted(WAKE_WORDS, key=len, reverse=True):
        if wake in lower:
            idx = lower.find(wake)
            remainder = (text[:idx] + text[idx + len(wake):]).strip(" ,.")
            return remainder
    return None


def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good morning!"
    elif hour < 17:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    speak(f"{greeting} I'm {ASSISTANT_NAME}. Say 'Jarvis' before your command to wake me up.")


def run_voice_mode():
    greet()
    while True:
        heard = listen()
        if not heard:
            continue

        command = strip_wake_word(heard)
        if command is None:
            # wake word wasn't used, ignore this and keep listening
            continue

        if not command:
            speak("Yes? Go ahead.")
            continue

        if command.lower().strip() in ("exit", "quit", "stop jarvis", "bye"):
            speak("Okay, goodbye!")
            break

        reply = handle_command(command)
        speak(reply)


def run_text_mode():
    greet()
    while True:
        try:
            command = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if not command:
            continue
        if command.lower() in ("exit", "quit", "bye"):
            speak("Okay, goodbye!")
            break
        reply = handle_command(command)
        speak(reply)


if __name__ == "__main__":
    mode = None
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        choice = input("Select mode - 'voice' or 'text': ").strip().lower()
        mode = choice if choice in ("voice", "text") else ("voice" if USE_VOICE_INPUT_BY_DEFAULT else "text")

    if mode == "voice":
        run_voice_mode()
    else:
        run_text_mode()
