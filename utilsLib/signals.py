import json


from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from utilsLib.models import Notification

@receiver(post_save, sender=Notification)
def trigger_sse_on_notification(sender, instance, created, **kwargs):
    """Triggers SSE when a new notification is created."""
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notification_group",
            {
                "type": "send.notification",
                "message": json.dumps({
                    "user": instance.user.username,
                    "message": instance.message,
                    "timestamp": instance.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
            }
        )
