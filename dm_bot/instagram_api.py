import os
import requests

INSTAGRAM_ACCOUNTS_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

BASE_URL = "https://graph.facebook.com/v17.0"

def send_instagram_dm(recipient_id, message_text):
    url = F"{BASE_URL}/{INSTAGRAM_ACCOUNTS_ID}/messages"
    params = {
        "access_token" : ACCESS_TOKEN,
    }
    data = {
        "recipient" : {'id' : recipient_id},
        "message" : {'text' : message_text}
    }
    response = requests.get(url, params=params, json=data)
    return response.json()


def get_recent_dms():
    url = f"{BASE_URL}/{INSTAGRAM_ACCOUNTS_ID}/conversations"
    params = {
        "access_token" : ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json()