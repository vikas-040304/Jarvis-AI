"""
vlc_controller.py
Sends commands to VLC using VLC's built-in HTTP web interface.

ONE-TIME SETUP:
1. Open VLC
2. Tools -> Preferences -> bottom-left corner "Show settings: All"
3. Interface -> Main interfaces -> tick the "Web" checkbox
4. Interface -> Main interfaces -> Lua -> in the "Lua HTTP" password field,
   type the exact same password as VLC_HTTP_PASSWORD in config.py
5. Save and restart VLC
"""

import requests
from requests.auth import HTTPBasicAuth
from config import VLC_HTTP_HOST, VLC_HTTP_PASSWORD


def _send_command(command: str, extra_params: dict = None) -> requests.Response:
    url = f"{VLC_HTTP_HOST}/requests/status.xml"
    params = {"command": command}
    if extra_params:
        params.update(extra_params)
    return requests.get(url, params=params, auth=HTTPBasicAuth("", VLC_HTTP_PASSWORD), timeout=3)


def pause_or_resume() -> str:
    """VLC only has one play_pause command - it toggles based on current state."""
    try:
        _send_command("pl_pause")
        return "Toggled play/pause on VLC."
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to VLC's HTTP interface. Make sure VLC is open and the web interface is enabled."
    except Exception as e:
        return f"Couldn't send the command to VLC: {e}"


def stop() -> str:
    try:
        _send_command("pl_stop")
        return "Stopped VLC."
    except Exception as e:
        return f"Couldn't stop: {e}"


def volume_up() -> str:
    try:
        _send_command("volume", {"val": "+20"})
        return "Turned the volume up."
    except Exception as e:
        return f"Couldn't change volume: {e}"


def volume_down() -> str:
    try:
        _send_command("volume", {"val": "-20"})
        return "Turned the volume down."
    except Exception as e:
        return f"Couldn't change volume: {e}"


def next_video() -> str:
    try:
        _send_command("pl_next")
        return "Skipped to the next video."
    except Exception as e:
        return f"Couldn't skip: {e}"
