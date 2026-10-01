"""
whatsapp_controller.py
Sends WhatsApp messages via WhatsApp Web, using pywhatkit.
Your browser needs to already be logged into WhatsApp Web (scan the QR code once,
it stays logged in after that).
"""

import pywhatkit
from config import CONTACTS


def send_message(contact_name: str, message: str) -> str:
    contact_name = contact_name.strip().lower()

    if contact_name not in CONTACTS:
        return f"I don't have a number saved for '{contact_name}'. Add it to CONTACTS in config.py."

    phone_number = CONTACTS[contact_name]

    try:
        # opens WhatsApp Web, waits, then sends automatically and closes the tab
        pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=True)
        return f"Sent your message to {contact_name.title()}."
    except Exception as e:
        return f"Couldn't send the WhatsApp message: {e}"
