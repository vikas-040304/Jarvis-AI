"""
web_search_controller.py
Opens your default browser with a Google search for whatever you asked -
useful for "Jarvis search for X" style commands, distinct from smart_chat.py
(which answers directly instead of opening a browser tab).
"""

import webbrowser
import urllib.parse


def search_google(query: str) -> str:
    query = query.strip()
    if not query:
        return "What would you like me to search for?"

    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)
    return f"Searching Google for '{query}'."


def search_youtube(query: str) -> str:
    query = query.strip()
    if not query:
        return "What would you like me to search for on YouTube?"

    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    webbrowser.open(url)
    return f"Searching YouTube for '{query}'."
