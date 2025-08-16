from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os, json
from .models import InstagramDM
from .tasks import process_dm  # Celery task

@csrf_exempt
def webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        verify_token = os.getenv("INSTAGRAM_VERIFY_TOKEN")

        if mode == "subscribe" and token == verify_token:
            return HttpResponse(challenge)   # plain text required by Meta
        return JsonResponse({"error": "Invalid token"}, status=403)

    elif request.method == "POST":
        # parse JSON safely
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception as e:
            return JsonResponse({"error": "invalid_json", "details": str(e)}, status=400)

        print("Incoming webhook:", json.dumps(payload, indent=2))  # debug

        for entry in payload.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                message = messaging_event.get("message")
                if not message:
                    continue  # skip non-message events

                # collect values safely
                mid = message.get("mid")
                sender_id = messaging_event.get("sender", {}).get("id")
                text = message.get("text", "")
                timestamp = messaging_event.get("timestamp")

                # create and assign to `dm` (THIS was the missing piece)
                dm = InstagramDM.objects.create(
                    message_id=mid,
                    sender_id=sender_id,
                    message_text=text,
                    created_time=timestamp
                )

                # dispatch async task; fallback to sync if Celery not configured
                try:
                    process_dm.delay(dm.id)
                except Exception as e:
                    # helpful fallback for debugging / local dev
                    print("Celery dispatch failed, running process_dm synchronously:", e)
                    process_dm(dm.id)

        return JsonResponse({"status": "ok"})
