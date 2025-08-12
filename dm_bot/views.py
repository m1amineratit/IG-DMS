from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import InstagramDM
from .tasks import process_dm
import json
import os

@csrf_exempt
def webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        verify_token = os.getenv("INSTAGRAM_VERIFY_TOKEN")

        if mode == "subscribe" and token == verify_token:
            return JsonResponse(int(challenge), safe=False)
        else:
            return JsonResponse({"error": "Invalid verification token"}, status=403)

    elif request.method == "POST":
        payload = json.loads(request.body)
        for entry in payload.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                try:
                    dm = InstagramDM.objects.create(
                        message_id=messaging_event["message"]["mid"],
                        sender_id=messaging_event["sender"]["id"],
                        message_text=messaging_event["message"]["text"],
                        created_time=messaging_event["timestamp"]
                    )
                    process_dm.delay(dm.id)
                except KeyError:
                    continue
        return JsonResponse({"status": "ok"})
