from django.db import models

# Create your models here.


class InstagramDM(models.Model):
    message_id = models.CharField(max_length=100, unique=True)
    sender_id = models.CharField(max_length=150)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)
    reply_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"DM from {self.sender_id}: {self.message_text[:30]}"