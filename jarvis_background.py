"""
jarvis_background.py
Runs Jarvis with NO terminal window and NO console prompts - built for
double-click use, or for building into a standalone .exe with PyInstaller
(using --noconsole).

It always starts in voice mode (no mode prompt, since there's no console to
type into) and puts a small icon in the system tray (bottom-right, near the
clock) - right-click it and choose "Quit Jarvis" to close it.
"""

import threading
import datetime

import speech_recognition as sr
import pyttsx3

from command_router import handle_command
from config import ASSISTANT_NAME, TTS_RATE, TTS_VOLUME

WAKE_WORDS = ["hey jarvis", "jarvis"]

# ---------------- TTS SETUP ----------------
engine = pyttsx3.init()
engine.setProperty("rate", TTS_RATE)
engine.setProperty("volume", TTS_VOLUME)

for voice in engine.getProperty("voices"):
    if "david" in voice.name.lower() or "male" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break

recognizer = sr.Recognizer()
_running = True


def speak(text: str):
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""
    try:
        return recognizer.recognize_google(audio, language="en-IN")
    except (sr.UnknownValueError, sr.RequestError):
        return ""


def strip_wake_word(text: str):
    lower = text.lower()
    for wake in sorted(WAKE_WORDS, key=len, reverse=True):
        if wake in lower:
            idx = lower.find(wake)
            return (text[:idx] + text[idx + len(wake):]).strip(" ,.")
    return None


def voice_loop():
    global _running
    hour = datetime.datetime.now().hour
    greeting = "Good morning!" if hour < 12 else "Good afternoon!" if hour < 17 else "Good evening!"
    speak(f"{greeting} I'm {ASSISTANT_NAME}, running in the background. Say Jarvis to wake me.")

    while _running:
        heard = listen()
        if not heard:
            continue

        command = strip_wake_word(heard)
        if command is None:
            continue

        if not command:
            speak("Yes? Go ahead.")
            continue

        if command.lower().strip() in ("exit", "quit", "stop jarvis"):
            speak("Okay, shutting down.")
            _running = False
            break

        reply = handle_command(command)
        speak(reply)


def make_tray_icon():
    """Small cyan-ring system tray icon with a Quit option, so you can close
    Jarvis without ever needing a terminal window."""
    try:
        # pyrefly: ignore [missing-import]
        import pystray
        from PIL import Image, ImageDraw
    except ImportError:
        return None

    img = Image.new("RGB", (64, 64), color=(10, 10, 10))
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 56, 56), outline=(0, 200, 255), width=4)
    draw.ellipse((24, 24, 40, 40), fill=(0, 200, 255))

    def on_quit(icon, item):
        global _running
        _running = False
        icon.stop()

    menu = pystray.Menu(pystray.MenuItem("Quit Jarvis", on_quit))
    return pystray.Icon("jarvis", img, "Jarvis AI", menu)


if __name__ == "__main__":
    voice_thread = threading.Thread(target=voice_loop, daemon=True)
    voice_thread.start()

    tray = make_tray_icon()
    if tray:
        tray.run()   # blocks here to keep the app alive; Quit stops everything
    else:
        # pystray/Pillow not available - just keep the background thread alive
        voice_thread.join()
