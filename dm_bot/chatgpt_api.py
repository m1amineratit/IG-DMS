import os
import requests
from .models import InstagramDM

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_conversation_history(user_id, limit=5):
    history = InstagramDM.objects.filter(sender_id=user_id).order_by('-created_time')[:limit]
    messages = []
    for msg in reversed(history):
        role = "assistant" if msg.replied else "user"
        content = msg.reply_text if role == "assistant" else msg.message_text
        messages.append({"role": role, "content": content})
    return messages


def generate_reply(user_id, new_message, business_info):
    system_message = f"You are a virtual assistant for {business_info['name']}. " \
                     f"You should answer customers about {business_info['field']} in a friendly, professional way."

    # Build conversation history
    messages = [{"role": "system", "content": system_message}]
    messages.extend(get_conversation_history(user_id))
    messages.append({"role": "user", "content": new_message})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",  # You can change to another model if needed
        "messages": messages,
        "max_tokens": 150
    }

    response = requests.post(OPENROUTER_URL, json=data, headers=headers)

    if response.status_code == 200:
        resp_json = response.json()
        return resp_json['choices'][0]['message']['content']
    else:
        return "Sorry, I couldn't generate a reply."
