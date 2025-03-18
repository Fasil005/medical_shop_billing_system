from django.urls import path
from inventory.views import (
    CategoryListAPIView,
    MedicineManagementAPIView,
    MedicineDetailedAPIView
)

urlpatterns = [
    path('', MedicineManagementAPIView.as_view()),
    path('<int:id>/', MedicineDetailedAPIView.as_view()),

    path('category/', CategoryListAPIView.as_view(), name='category_list')
]
