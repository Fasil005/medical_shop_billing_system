from django.urls import path
from users.views import UserListAPIView, UserDetailedAPIView

urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('<int:id>/', UserDetailedAPIView.as_view()),
]
