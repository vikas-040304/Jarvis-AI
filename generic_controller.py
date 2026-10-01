"""
generic_controller.py
Sends common keyboard shortcuts to whichever window currently has focus.
This is how Jarvis can control features INSIDE almost any app (browser,
VS Code, Word, File Explorer, etc.) without needing custom integration for
every single app - most apps share the same standard shortcuts.

Important: these commands act on whatever window is currently active/focused
on your screen at the moment you say them - not a specific named app.
"""

import pyautogui

pyautogui.FAILSAFE = True  # move mouse to a screen corner to abort, as a safety net


def new_tab():
    pyautogui.hotkey("ctrl", "t")
    return "Opened a new tab."


def close_tab():
    pyautogui.hotkey("ctrl", "w")
    return "Closed the tab."


def next_tab():
    pyautogui.hotkey("ctrl", "tab")
    return "Switched to the next tab."


def previous_tab():
    pyautogui.hotkey("ctrl", "shift", "tab")
    return "Switched to the previous tab."


def refresh():
    pyautogui.press("f5")
    return "Refreshed."


def find():
    pyautogui.hotkey("ctrl", "f")
    return "Opened find - type what you're looking for."


def save():
    pyautogui.hotkey("ctrl", "s")
    return "Saved."


def undo():
    pyautogui.hotkey("ctrl", "z")
    return "Undone."


def redo():
    pyautogui.hotkey("ctrl", "y")
    return "Redone."


def copy():
    pyautogui.hotkey("ctrl", "c")
    return "Copied."


def paste():
    pyautogui.hotkey("ctrl", "v")
    return "Pasted."


def select_all():
    pyautogui.hotkey("ctrl", "a")
    return "Selected everything."


def zoom_in():
    pyautogui.hotkey("ctrl", "+")
    return "Zoomed in."


def zoom_out():
    pyautogui.hotkey("ctrl", "-")
    return "Zoomed out."


def minimize_window():
    pyautogui.hotkey("win", "down")
    return "Minimized the window."


def maximize_window():
    pyautogui.hotkey("win", "up")
    return "Maximized the window."


def close_window():
    pyautogui.hotkey("alt", "f4")
    return "Closed the window."


def switch_window():
    pyautogui.hotkey("alt", "tab")
    return "Switched windows."


def scroll_up():
    pyautogui.scroll(500)
    return "Scrolled up."


def scroll_down():
    pyautogui.scroll(-500)
    return "Scrolled down."


def go_back():
    pyautogui.hotkey("alt", "left")
    return "Went back."


def go_forward():
    pyautogui.hotkey("alt", "right")
    return "Went forward."


def go_home():
    pyautogui.hotkey("alt", "home")
    return "Went to the home page."


def full_screen():
    pyautogui.press("f11")
    return "Toggled full screen."


def print_this():
    pyautogui.hotkey("ctrl", "p")
    return "Opened the print dialog."


def new_window():
    pyautogui.hotkey("ctrl", "n")
    return "Opened a new window."


def reopen_closed_tab():
    pyautogui.hotkey("ctrl", "shift", "t")
    return "Reopened the last closed tab."


def volume_up():
    pyautogui.press("volumeup")
    return "Turned the system volume up."


def volume_down():
    pyautogui.press("volumedown")
    return "Turned the system volume down."


def mute():
    pyautogui.press("volumemute")
    return "Toggled mute."


def play_pause_media():
    """Works with the media keys most keyboards/laptops send - controls whatever
    media app (Spotify, YouTube, VLC, etc.) is currently playing."""
    pyautogui.press("playpause")
    return "Toggled play/pause."


def set_volume(percent: int) -> str:
    """Sets the system volume to an exact percentage (0-100), using pycaw."""
    percent = max(0, min(100, percent))
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
        return f"Set the volume to {percent} percent."
    except ImportError:
        return "The pycaw library isn't installed. Run: pip install pycaw"
    except Exception as e:
        return f"Couldn't set the volume: {e}"
