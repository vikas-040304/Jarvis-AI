"""
system_controller.py
Handles system-level commands: shutdown, restart, lock screen, screenshot.
"""

import subprocess
import ctypes
import datetime
from pathlib import Path

SHUTDOWN_DELAY = 10  # seconds - gives you time to cancel


def shutdown() -> str:
    subprocess.run(["shutdown", "/s", "/t", str(SHUTDOWN_DELAY)], shell=True)
    return f"Shutting down in {SHUTDOWN_DELAY} seconds. Say 'cancel shutdown' to stop it."


def restart() -> str:
    subprocess.run(["shutdown", "/r", "/t", str(SHUTDOWN_DELAY)], shell=True)
    return f"Restarting in {SHUTDOWN_DELAY} seconds. Say 'cancel shutdown' to stop it."


def cancel_shutdown() -> str:
    subprocess.run(["shutdown", "/a"], shell=True)
    return "Shutdown/restart cancelled."


def lock() -> str:
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Locking the screen."
    except Exception as e:
        return f"Couldn't lock the screen: {e}"


def screenshot() -> str:
    try:
        from PIL import ImageGrab
    except ImportError:
        return "Pillow isn't installed. Run: pip install Pillow"

    folder = Path.home() / "Pictures" / "JarvisScreenshots"
    folder.mkdir(parents=True, exist_ok=True)
    filename = folder / f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    try:
        img = ImageGrab.grab()
        img.save(filename)
        return f"Screenshot saved to {filename}"
    except Exception as e:
        return f"Couldn't take a screenshot: {e}"
