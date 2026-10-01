"""
spotify_controller.py
Handles opening Spotify and playing/controlling songs, using the Spotify Web API
(via spotipy). The Spotify desktop app needs to already be open on your computer
(as an active device) for playback control to work.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

_sp = None


def _get_client():
    global _sp
    if _sp is None:
        _sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-modify-playback-state user-read-playback-state"
        ))
    return _sp


def play_song(song_name: str) -> str:
    try:
        sp = _get_client()
        results = sp.search(q=song_name, limit=1, type="track")
        tracks = results["tracks"]["items"]
        if not tracks:
            return f"Couldn't find a song called '{song_name}' on Spotify."

        track = tracks[0]
        track_uri = track["uri"]
        track_title = track["name"]
        artist = track["artists"][0]["name"]

        devices = sp.devices()["devices"]
        if not devices:
            return "Open the Spotify app first, then I'll be able to see a device."

        device_id = devices[0]["id"]
        sp.start_playback(device_id=device_id, uris=[track_uri])
        return f"Playing '{track_title}' by {artist}."
    except Exception as e:
        return f"Couldn't play that song on Spotify: {e}"


def pause() -> str:
    try:
        _get_client().pause_playback()
        return "Paused Spotify."
    except Exception as e:
        return f"Couldn't pause: {e}"


def resume() -> str:
    try:
        _get_client().start_playback()
        return "Resumed Spotify."
    except Exception as e:
        return f"Couldn't resume: {e}"


def next_track() -> str:
    try:
        _get_client().next_track()
        return "Skipped to the next song."
    except Exception as e:
        return f"Couldn't skip: {e}"


def previous_track() -> str:
    try:
        _get_client().previous_track()
        return "Went back to the previous song."
    except Exception as e:
        return f"Couldn't go back: {e}"
