from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification(request):
    if request.method == 'POST':
        message = request.POST.get('message', 'Hello, World!')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                'type': 'notification_message',
                'message': message
            }
        )
        return JsonResponse({"status": "Notification sent!", "message": message})
    return JsonResponse({"error": "Only POST requests are allowed."}, status=400)
