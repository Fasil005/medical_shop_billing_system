from django.urls import path

from inventory.views import (
    InvoiceManagementAPIView
)


urlpatterns = [
    path('', InvoiceManagementAPIView.as_view()),
]