from django.urls import path
from django.views.decorators.http import require_GET

from inventory.views import (
    StockManagementAPIView,
    StaffSalesReportAPIView,
    DashboardMetricsAPIView
)
from inventory.models import MedicineStock
from inventory.serializers import DashboardStockSerializer
from utilsLib.permissions import AdminPermission


urlpatterns = [
    path('stocks/', require_GET(StockManagementAPIView.as_view(
        queryset=MedicineStock.objects.filter(stock__gt=0).select_related('medicine', 'created_by', 'packaging'),
        permission_classes=[AdminPermission],
        serializer_class = DashboardStockSerializer,
    ))),
    path('reports/staff-sale/', StaffSalesReportAPIView.as_view()),
    path('reports/', DashboardMetricsAPIView.as_view()),
]