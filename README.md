# Jarvis AI - Setup Guide

Your own Iron Man-style personal assistant for Windows: opens apps, controls
Spotify and VLC, sends WhatsApp messages, controls your system, and answers
general questions using Google Gemini (free).

## 1. What's in the project

| File | What it does |
|---|---|
| `jarvis.py` | Main file - run this (asks voice/text, shows a terminal) |
| `jarvis_background.py` | No-terminal version - always voice mode, quits from the system tray |
| `command_router.py` | Understands your command and routes it to the right action |
| `app_launcher.py` | Opens apps (Chrome, Notepad, Spotify, etc.) |
| `spotify_controller.py` | Spotify open/play/pause/next/previous |
| `vlc_controller.py` | VLC pause/resume/stop/volume |
| `system_controller.py` | Shutdown, restart, lock screen, screenshot |
| `whatsapp_controller.py` | Sends WhatsApp messages via WhatsApp Web |
| `generic_controller.py` | Controls features inside whatever app is currently active (tabs, save, find, zoom, scroll, browser nav, system volume, etc.) |
| `web_search_controller.py` | Opens a Google or YouTube search in your browser |
| `screen_reader.py` | Takes a screenshot and asks Gemini to explain what's on screen |
| `smart_chat.py` | Falls back to Gemini for general questions ("what's the capital of France") |
| `config.py` | **Fill this in first** - API keys, passwords, app paths, contacts |
| `build_exe.bat` | One-click script to package Jarvis into a standalone .exe |
| `requirements.txt` | Libraries to install |

## 2. Install Python (if you don't have it)

Get it from https://python.org - during install, tick **"Add Python to PATH"**.

## 3. Install the libraries

Open Command Prompt, go to the `jarvis_ai` folder, and run:

```
pip install -r requirements.txt
```

> ⚠️ If `pyaudio` fails to install (common on Windows):
> ```
> pip install pipwin
> pipwin install pyaudio
> ```

## 4. Fill in config.py

### Spotify setup (~2 min):
1. Go to https://developer.spotify.com/dashboard and log in
2. Click "Create app"
3. Set the Redirect URI to exactly: `http://127.0.0.1:8888/callback`
4. Copy the Client ID and Client Secret into `config.py`

### VLC setup (~1 min):
1. Open VLC
2. Tools → Preferences → bottom-left "Show settings: All"
3. Interface → Main interfaces → tick the "Web" checkbox
4. Interface → Main interfaces → Lua → set a password matching
   `VLC_HTTP_PASSWORD` in `config.py` (default: `jarvis123`)
5. Save and restart VLC

### Gemini API key (for smart chat) - FREE:
1. Go to https://aistudio.google.com/app/apikey and sign in with a Google account
2. Click "Create API key" - no credit card needed
3. Paste it into `GEMINI_API_KEY` in `config.py`
4. Free tier gives roughly 1,500 requests/day - plenty for personal use
5. Newer keys start with `AQ.Ab...` instead of the old `AIza...` format - that's
   normal, just paste whatever AI Studio gives you

### WhatsApp contacts:
Add names and phone numbers (with country code) to `CONTACTS` in `config.py`, e.g.:
```python
CONTACTS = {
    "amma": "+91XXXXXXXXXX",
    "friend": "+919876543210",
}
```
The first time you send a message, a browser tab will open to WhatsApp Web -
scan the QR code once with your phone, and it'll stay logged in after that.

### App paths:
Check `APP_PATHS` in `config.py` - update any exe paths that are different on
your computer (especially Steam, Bluestacks, Telegram, Zoom).

## 5. Run it

```
python jarvis.py
```

It'll ask `Select mode - 'voice' or 'text'`. Or skip straight to one:
```
python jarvis.py voice
python jarvis.py text
```

## 6. How to talk to it

**Voice mode now needs a wake word** - say **"Jarvis"** (or "Hey Jarvis")
somewhere in your sentence, or it'll ignore you and keep listening quietly.
This stops it from reacting to background conversation.

- "Jarvis, open spotify"
- "Jarvis play Blinding Lights on spotify"
- "Jarvis pause spotify" / "Jarvis resume spotify"
- "Jarvis vlc pause" / "Jarvis vlc resume"
- "Jarvis volume up on vlc"
- "Jarvis open notepad" / "Jarvis open vs code"
- "Jarvis what's the time" / "Jarvis what's the date"
- "Jarvis shutdown" / "Jarvis restart" / "Jarvis cancel shutdown"
- "Jarvis lock the screen"
- "Jarvis take a screenshot"
- "Jarvis send message to amma saying I'll be home soon"
- "Jarvis what's the capital of France" → falls back to Gemini for an answer

**In-app control** - these act on whatever window is currently active/focused
on your screen (works across most browsers, editors, and apps that use
standard shortcuts):
- "Jarvis new tab" / "Jarvis close tab" / "Jarvis next tab" / "Jarvis previous tab"
- "Jarvis reopen tab" / "Jarvis new window"
- "Jarvis go back" / "Jarvis go forward" / "Jarvis go home"
- "Jarvis refresh" / "Jarvis full screen" / "Jarvis print this"
- "Jarvis save this" / "Jarvis undo" / "Jarvis redo"
- "Jarvis copy this" / "Jarvis paste this" / "Jarvis select all"
- "Jarvis zoom in" / "Jarvis zoom out"
- "Jarvis minimize this" / "Jarvis maximize this" / "Jarvis close this window"
- "Jarvis switch window" / "Jarvis scroll up" / "Jarvis scroll down"
- "Jarvis turn up the volume" / "Jarvis turn down the volume" / "Jarvis mute"

**Web search:**
- "Jarvis search for best budget phones 2026" → opens a Google search
- "Jarvis search youtube for lofi music" → opens a YouTube search

**Screen reader** - describes or explains whatever is currently visible:
- "Jarvis what's on my screen"
- "Jarvis explain this error"

**Text mode doesn't need the wake word** - just type your command directly.

## 7. Safety notes

- **Shutdown/restart give you a 10-second warning** before they happen - say
  "Jarvis cancel shutdown" during that window to stop it.
- WhatsApp sending opens a real browser tab and sends automatically - double
  check the contact/message before you say the command.

## 8. Honest limitations

- Voice recognition uses Google's online API (`en-IN` language) - needs
  internet, and works best with clear English.
- TTS uses your Windows voices - male voice ("David") is auto-selected if
  available.
- Spotify control needs the Spotify desktop app already open.
- Command understanding is mostly keyword-matching for known actions; anything
  it doesn't recognize now gets sent to Gemini instead of failing outright.
- The wake word check happens after speech is already sent to Google for
  transcription each time - it's not a true low-power wake word, just a filter
  on the result.

## 9. Running without a terminal (looks like a real app)

By default `jarvis.py` needs a terminal window and asks "voice or text" every
time. `jarvis_background.py` skips all of that - it starts straight into
voice mode with no console prompts, and puts a small icon in your system tray
(bottom-right, near the clock) so you can right-click → "Quit Jarvis" to
close it.

**Option 1 - run it as a Python script (no terminal popup needed):**
```
pyw jarvis_background.py
```
(`pyw` runs Python without opening a console window at all.)

**Option 2 - build it into a real Jarvis.exe (double-click to launch):**
1. Make sure `pyinstaller` is installed (already in `requirements.txt`)
2. Double-click `build_exe.bat`, or run:
   ```
   py -3.13 -m PyInstaller --onefile --noconsole --name Jarvis jarvis_background.py
   ```
3. Your `Jarvis.exe` appears inside the new `dist` folder
4. Copy `Jarvis.exe` anywhere you like (Desktop, Start Menu folder, etc.) and
   double-click it - it behaves like a normal Windows app, no terminal at all

**Want it to auto-start with Windows?** Press `Win + R`, type `shell:startup`,
and drop a shortcut to `Jarvis.exe` in that folder - it'll launch every time
you log in.

## 10. Getting the Iron Man HUD desktop look

The circular glowing HUD look (rings, arc reactor, weather panel) isn't
something built into this Python project - it's a separate desktop
customization tool called **Rainmeter**, and free "JARVIS" / "S.H.I.E.L.D OS"
skins already exist for it that match that look closely.

1. Install Rainmeter from https://www.rainmeter.net
2. Download a JARVIS-style skin, e.g. "S.H.I.E.L.D OS" by eApathy on DeviantArt
3. Extract the skin files into `C:\Users\<you>\Documents\Rainmeter\Skins`
4. Open Rainmeter's manage window and apply the included layout
5. Adjust the `.ini` files for your weather location, drive letters, etc.

Run this alongside `Jarvis.exe` (set both to auto-start) and you'll have the
glowing HUD desktop *and* a working voice assistant at the same time - just
like the movie, minus the terminal window.

## 11. Ideas for later

- A proper offline wake word using `pvporcupine` (so it's not always sending
  audio to Google)
- Reminders/alarms
- Reading out unread emails or messages
