from .chatgpt_api import generate_reply
from .instagram_api import send_instagram_dm
from .models import InstagramDM

def process_dm(dm_id):
    dm = InstagramDM.objects.get(id=dm_id)

    # 1. Generate AI reply
    reply = generate_reply(dm.message_text, {})

    # 2. Send reply to the correct user (not the whole object)
    send_instagram_dm(dm.sender_id, reply)  # ✅ sender_id must exist in your model

    # 3. Update the database record
    dm.replied = True
    dm.reply_text = reply
    dm.save()
