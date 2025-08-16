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
    system_message = (
        f"You are a virtual assistant for {business_info.get('name', 'our business')}. "
        f"Answer customers about {business_info.get('field', 'our services')} "
        f"in a friendly, professional way."
    )

    # Build conversation history
    messages = [{"role": "system", "content": system_message}]
    messages.extend(get_conversation_history(user_id))
    messages.append({"role": "user", "content": new_message})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",  # could also try "gpt-4o" or "llama-3.1-70b"
        "messages": messages,
        "max_tokens": 150,
    }

    response = requests.post(OPENROUTER_URL, json=data, headers=headers)

    try:
        response.raise_for_status()
        resp_json = response.json()
        return resp_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("OpenRouter error:", e, response.text)
        return "Sorry, I couldn't generate a reply right now."
