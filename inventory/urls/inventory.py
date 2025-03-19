from django.urls import path
from inventory.views import (
    StockManagementAPIView,
    StockDetailedManagementAPIView,
    MedicinePackageManagementAPIView,
    MedicinePackageDetailedManagementAPIView,
    SupplierManagementAPIView,
    SupplierDetailedManagementAPIView
)

urlpatterns = [
    path('packaging/',  MedicinePackageManagementAPIView.as_view()),
    path('packaging/<int:id>/',  MedicinePackageDetailedManagementAPIView.as_view()),

    path('supplier/', SupplierManagementAPIView.as_view()),
    path('supplier/<int:id>/', SupplierDetailedManagementAPIView.as_view()),

    path('stocks/', StockManagementAPIView.as_view()),
    path('stocks/<int:id>/', StockDetailedManagementAPIView.as_view()),
]
