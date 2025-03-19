import json
import time

from django.http import StreamingHttpResponse
from django.utils.timezone import localtime

from rest_framework.views import APIView

from utilsLib.models import Notification

class SSENotificationsAPIView(APIView):
    """Streams new unread notifications in real-time using Server-Sent Events (SSE)."""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return StreamingHttpResponse("data: Unauthorized\n\n", content_type='text/event-stream', status=403)

        response = StreamingHttpResponse(self.event_stream(request.user), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    def event_stream(self, user):
        """Continuously stream new unread notifications to the client."""
        while True:
            time.sleep(1)  # Prevent excessive CPU usage
            
            unread_notifications = Notification.objects.filter(user=user, is_read=False).order_by('created_at')

            if unread_notifications.exists():
                for notification in unread_notifications:
                    notification_time = localtime(notification.created_at)
                    message = json.dumps({
                        "user": notification.user.username,
                        "message": notification.message,
                        "timestamp": notification_time.strftime('%Y-%m-%d %H:%M:%S')
                    })

                    # Mark notification as read after sending
                    notification.is_read = True
                    notification.save(update_fields=["is_read"])

                    yield f"data: {message}\n\n"
