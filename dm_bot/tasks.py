from .chatgpt_api import generate_reply
from .instagram_api import send_instagram_dm
from .models import InstagramDM

def process_dm(dm_id):
    dm = InstagramDM.objects.get(id=dm_id)
    reply = generate_reply(dm.message_text, {})
    send_instagram_dm(reply, dm)
    dm.replied = True
    dm.reply_text = reply
    dm.save()