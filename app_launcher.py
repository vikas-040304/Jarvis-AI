"""
app_launcher.py
Handles opening Windows apps.
"""

import os
import subprocess
import webbrowser
from config import APP_PATHS


def open_app(app_name: str) -> str:
    """
    app_name: name spoken/typed by the user (matched case-insensitively)
    returns: a reply string for Jarvis to say/print
    """
    app_name = app_name.strip().lower()

    # find nearest match (exact or partial)
    matched_key = None
    for key in APP_PATHS:
        if key in app_name or app_name in key:
            matched_key = key
            break

    if not matched_key:
        return f"I couldn't find an app called '{app_name}'. Add it to config.py."

    path = APP_PATHS[matched_key]
    path = os.path.expandvars(path)  # resolves things like %USERNAME%

    try:
        if path.startswith("http://") or path.startswith("https://"):
            webbrowser.open(path)
        elif path.endswith(":"):
            # UWP / protocol style apps (spotify:, whatsapp:, microsoft.windows.camera:)
            os.startfile(path)
        elif path in ("calc.exe", "notepad.exe", "explorer.exe", "winword.exe", "wt.exe", "code"):
            subprocess.Popen(path, shell=True)
        else:
            subprocess.Popen([path])
        return f"Opening {matched_key.title()}."
    except FileNotFoundError:
        return f"Couldn't find the correct path for {matched_key.title()}. Check APP_PATHS in config.py."
    except Exception as e:
        return f"Tried to open {matched_key.title()}, but got an error: {e}"
