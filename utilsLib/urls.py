from django.urls import path

from utilsLib.views import SSENotificationsAPIView

urlpatterns = [
    path("", SSENotificationsAPIView.as_view(), name="sse-notifications"),
]
