"""
command_router.py
Parses the user's typed/spoken text (English) and routes it to the right action.
"""

import re
import datetime

from app_launcher import open_app
import spotify_controller as spotify
import vlc_controller as vlc
import system_controller as system
import whatsapp_controller as whatsapp
import generic_controller as generic
import screen_reader
import web_search_controller as web_search
import smart_chat

# Keyword sets for each intent
OPEN_WORDS = ["open", "launch", "start"]
PLAY_WORDS = ["play"]
PAUSE_WORDS = ["pause", "hold"]
RESUME_WORDS = ["resume", "continue"]
STOP_WORDS = ["stop"]
NEXT_WORDS = ["next", "skip"]
PREV_WORDS = ["previous", "back", "prev"]
VOLUME_UP_WORDS = ["volume up", "increase volume", "louder"]
VOLUME_DOWN_WORDS = ["volume down", "decrease volume", "quieter"]
DATE_WORDS = ["date", "what's the date", "today's date"]
TIME_WORDS = ["time", "what time", "current time"]

SHUTDOWN_WORDS = ["shutdown", "shut down", "turn off the computer", "turn off the pc"]
RESTART_WORDS = ["restart", "reboot"]
CANCEL_SHUTDOWN_WORDS = ["cancel shutdown", "cancel restart", "stop shutdown"]
LOCK_WORDS = ["lock the screen", "lock screen", "lock my pc", "lock computer"]
SCREENSHOT_WORDS = ["screenshot", "take a screenshot", "capture screen"]

# ---- GENERIC IN-APP CONTROL (works on whatever window is currently active) ----
NEW_TAB_WORDS = ["new tab"]
CLOSE_TAB_WORDS = ["close tab", "close this tab"]
NEXT_TAB_WORDS = ["next tab"]
PREV_TAB_WORDS = ["previous tab", "prev tab"]
REFRESH_WORDS = ["refresh", "reload"]
FIND_WORDS = ["find on this page", "find on page", "search this page", "search on this page"]
SAVE_WORDS = ["save this", "save the file", "save file", "save it"]
UNDO_WORDS = ["undo"]
REDO_WORDS = ["redo"]
COPY_WORDS = ["copy this", "copy it"]
PASTE_WORDS = ["paste this", "paste it"]
SELECT_ALL_WORDS = ["select all"]
ZOOM_IN_WORDS = ["zoom in"]
ZOOM_OUT_WORDS = ["zoom out"]
MINIMIZE_WORDS = ["minimize this", "minimize window", "minimise this", "minimise window"]
MAXIMIZE_WORDS = ["maximize this", "maximize window", "maximise this", "maximise window"]
CLOSE_WINDOW_WORDS = ["close this window", "close the window"]
SWITCH_WINDOW_WORDS = ["switch window", "switch app", "alt tab"]
SCROLL_UP_WORDS = ["scroll up"]
SCROLL_DOWN_WORDS = ["scroll down"]

GO_BACK_WORDS = ["go back"]
GO_FORWARD_WORDS = ["go forward"]
GO_HOME_WORDS = ["go home", "go to homepage"]
FULL_SCREEN_WORDS = ["full screen", "fullscreen"]
PRINT_WORDS = ["print this", "print it"]
NEW_WINDOW_WORDS = ["new window"]
REOPEN_TAB_WORDS = ["reopen tab", "reopen closed tab", "reopen last tab"]

SYSTEM_VOLUME_UP_WORDS = ["turn up the volume", "increase system volume", "volume up"]
SYSTEM_VOLUME_DOWN_WORDS = ["turn down the volume", "decrease system volume", "volume down"]
MUTE_WORDS = ["mute", "mute the sound", "mute audio"]

SCREEN_READ_WORDS = [
    "what's on my screen", "whats on my screen", "read my screen",
    "explain my screen", "what is on the screen", "read the screen",
    "explain this screen", "what's this", "explain this error", "read this error",
]

# e.g. "set volume to 50" / "set the volume to 50 percent"
SET_VOLUME_PATTERN = re.compile(r"(?:set (?:the )?volume to|volume to)\s+(\d{1,3})")

# e.g. "search for best laptops 2026" / "google best laptops"
GOOGLE_SEARCH_PATTERN = re.compile(r"(?:search google for|google search for|search for|google)\s+(.+)")
# e.g. "search youtube for lofi music"
YOUTUBE_SEARCH_PATTERN = re.compile(r"(?:search youtube for|youtube search for|search on youtube for)\s+(.+)")

# e.g. "send message to amma saying I'll be late"
# e.g. "whatsapp appa call me back"
WHATSAPP_PATTERN = re.compile(
    r"(?:send (?:a )?(?:whatsapp )?message to|whatsapp)\s+(\w+)\s+(?:saying|that says|:)?\s*(.+)"
)


def _contains_any(text: str, words: list) -> bool:
    return any(w in text for w in words)


def _extract_after_keyword(text: str, keywords: list) -> str:
    """e.g. 'play Blinding Lights on spotify' -> 'Blinding Lights' (rough heuristic)."""
    for kw in keywords:
        if kw in text:
            remainder = text.split(kw, 1)[1].strip()
            for filler in (" song", " on spotify", " in spotify", " spotify"):
                remainder = remainder.replace(filler, "")
            return remainder.strip()
    return text.strip()


def handle_command(user_text: str) -> str:
    """
    Main entry point. user_text = recognized speech or typed text (English).
    Returns Jarvis's reply (English).
    """
    text = user_text.lower().strip()

    if not text:
        return "I didn't catch that, please say it again."

    # ---- DATE / TIME ----
    if _contains_any(text, TIME_WORDS) and "spotify" not in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"It's currently {now}."

    if _contains_any(text, DATE_WORDS):
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today's date is {today}."

    # ---- SYSTEM CONTROL ----
    if _contains_any(text, CANCEL_SHUTDOWN_WORDS):
        return system.cancel_shutdown()
    if _contains_any(text, SHUTDOWN_WORDS):
        return system.shutdown()
    if _contains_any(text, RESTART_WORDS):
        return system.restart()
    if _contains_any(text, LOCK_WORDS):
        return system.lock()
    if _contains_any(text, SCREENSHOT_WORDS):
        return system.screenshot()

    # ---- WHATSAPP ----
    match = WHATSAPP_PATTERN.search(text)
    if match:
        contact_name, message = match.groups()
        return whatsapp.send_message(contact_name, message)

    # ---- SPOTIFY ----
    if "spotify" in text:
        if _contains_any(text, PAUSE_WORDS):
            return spotify.pause()
        if _contains_any(text, RESUME_WORDS):
            return spotify.resume()
        if _contains_any(text, NEXT_WORDS):
            return spotify.next_track()
        if _contains_any(text, PREV_WORDS):
            return spotify.previous_track()
        if _contains_any(text, PLAY_WORDS) or _contains_any(text, OPEN_WORDS):
            song = _extract_after_keyword(text, PLAY_WORDS + ["spotify"])
            if song and song != "spotify":
                return spotify.play_song(song)
            return open_app("spotify")

    # ---- VLC ----
    if "vlc" in text or "video" in text:
        if _contains_any(text, PAUSE_WORDS) or _contains_any(text, RESUME_WORDS):
            return vlc.pause_or_resume()
        if _contains_any(text, STOP_WORDS):
            return vlc.stop()
        if _contains_any(text, VOLUME_UP_WORDS):
            return vlc.volume_up()
        if _contains_any(text, VOLUME_DOWN_WORDS):
            return vlc.volume_down()
        if _contains_any(text, NEXT_WORDS):
            return vlc.next_video()
        if _contains_any(text, OPEN_WORDS):
            return open_app("vlc")

    # ---- GENERIC APP OPEN ----
    if _contains_any(text, OPEN_WORDS):
        app_name = _extract_after_keyword(text, OPEN_WORDS)
        if app_name:
            return open_app(app_name)

    # ---- SET EXACT VOLUME ----
    volume_match = SET_VOLUME_PATTERN.search(text)
    if volume_match:
        return generic.set_volume(int(volume_match.group(1)))

    # ---- WEB / YOUTUBE SEARCH ----
    yt_match = YOUTUBE_SEARCH_PATTERN.search(text)
    if yt_match:
        return web_search.search_youtube(yt_match.group(1))

    google_match = GOOGLE_SEARCH_PATTERN.search(text)
    if google_match:
        return web_search.search_google(google_match.group(1))

    # ---- SCREEN READER ----
    if _contains_any(text, SCREEN_READ_WORDS):
        return screen_reader.read_screen()

    # ---- GENERIC IN-APP CONTROL (acts on whatever window is active) ----
    if _contains_any(text, NEW_TAB_WORDS):
        return generic.new_tab()
    if _contains_any(text, CLOSE_TAB_WORDS):
        return generic.close_tab()
    if _contains_any(text, NEXT_TAB_WORDS):
        return generic.next_tab()
    if _contains_any(text, PREV_TAB_WORDS):
        return generic.previous_tab()
    if _contains_any(text, REOPEN_TAB_WORDS):
        return generic.reopen_closed_tab()
    if _contains_any(text, REFRESH_WORDS):
        return generic.refresh()
    if _contains_any(text, FIND_WORDS):
        return generic.find()
    if _contains_any(text, SAVE_WORDS):
        return generic.save()
    if _contains_any(text, UNDO_WORDS):
        return generic.undo()
    if _contains_any(text, REDO_WORDS):
        return generic.redo()
    if _contains_any(text, COPY_WORDS):
        return generic.copy()
    if _contains_any(text, PASTE_WORDS):
        return generic.paste()
    if _contains_any(text, SELECT_ALL_WORDS):
        return generic.select_all()
    if _contains_any(text, ZOOM_IN_WORDS):
        return generic.zoom_in()
    if _contains_any(text, ZOOM_OUT_WORDS):
        return generic.zoom_out()
    if _contains_any(text, MINIMIZE_WORDS):
        return generic.minimize_window()
    if _contains_any(text, MAXIMIZE_WORDS):
        return generic.maximize_window()
    if _contains_any(text, CLOSE_WINDOW_WORDS):
        return generic.close_window()
    if _contains_any(text, SWITCH_WINDOW_WORDS):
        return generic.switch_window()
    if _contains_any(text, SCROLL_UP_WORDS):
        return generic.scroll_up()
    if _contains_any(text, SCROLL_DOWN_WORDS):
        return generic.scroll_down()
    if _contains_any(text, GO_BACK_WORDS):
        return generic.go_back()
    if _contains_any(text, GO_FORWARD_WORDS):
        return generic.go_forward()
    if _contains_any(text, GO_HOME_WORDS):
        return generic.go_home()
    if _contains_any(text, FULL_SCREEN_WORDS):
        return generic.full_screen()
    if _contains_any(text, PRINT_WORDS):
        return generic.print_this()
    if _contains_any(text, NEW_WINDOW_WORDS):
        return generic.new_window()
    if _contains_any(text, MUTE_WORDS):
        return generic.mute()
    if _contains_any(text, SYSTEM_VOLUME_UP_WORDS) and "vlc" not in text:
        return generic.volume_up()
    if _contains_any(text, SYSTEM_VOLUME_DOWN_WORDS) and "vlc" not in text:
        return generic.volume_down()

    # ---- FALLBACK: SMART CHAT (Gemini) ----
    return smart_chat.ask_claude(user_text)
