# ============================================
# JARVIS AI - CONFIG FILE
# Fill in your details below
# ============================================

# ---- SPOTIFY SETTINGS ----
# Create an app at https://developer.spotify.com/dashboard
# Add this as the Redirect URI: http://127.0.0.1:8888/callback
SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

# ---- VLC SETTINGS ----
# Open VLC -> Tools -> Preferences -> Show settings: ALL (bottom left)
# -> Interface -> Main interfaces -> tick the "Web" checkbox
# -> Interface -> Main interfaces -> Lua -> set a password in the password field
VLC_HTTP_HOST = "http://localhost:8080"
VLC_HTTP_PASSWORD = "jarvis123"   # must match the password you set in VLC's Lua interface

# ---- GEMINI (SMART CHAT) SETTINGS - FREE, no credit card needed ----
# Get your free API key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY = ""

# ---- WHATSAPP CONTACTS ----
# name -> phone number with country code (e.g. India = +91)
CONTACTS = {
    "amma": "+91XXXXXXXXXX",
    "appa": "+91XXXXXXXXXX",
    "friend": "+91XXXXXXXXXX",
}

# ---- ASSISTANT NAME ----
ASSISTANT_NAME = "Jarvis"

# ---- VOICE SETTINGS ----
USE_VOICE_INPUT_BY_DEFAULT = True   # set False to start in text mode instead
TTS_RATE = 175          # speaking speed
TTS_VOLUME = 1.0

# ---- APP PATHS ----
# If an app's exe path is different on your computer, update it here.
# Apps already registered in the Start Menu (calc, notepad, mspaint) don't need a
# full path, but apps like Steam, Bluestacks, etc. need the exact install path.
APP_PATHS = {
    "brave browser": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "calculator": "calc.exe",
    "camera": "microsoft.windows.camera:",
    "canva": "https://www.canva.com",              # opens in browser
    "chatgpt": "https://chat.openai.com",           # opens in browser
    "chatgpt classic": "https://chat.openai.com",
    "claude": "https://claude.ai",
    "git": r"C:\Program Files\Git\git-bash.exe",
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "notepad": "notepad.exe",
    "vs code": "code",
    "visual studio code": "code",
    "file explorer": "explorer.exe",
    "spotify": "spotify:",
    "telegram": r"C:\Users\%USERNAME%\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "terminal": "wt.exe",
    "whatsapp": "whatsapp:",
    "word": "winword.exe",
    "bluestacks": r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",
    "youtube": "https://www.youtube.com",
    "zoom": r"C:\Users\%USERNAME%\AppData\Roaming\Zoom\bin\Zoom.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
}
