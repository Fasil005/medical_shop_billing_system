from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from inventory.mixins import CreatedByMixin
from utilsLib.permissions import (
    InventoryManagerPermission,
    AdminPermission
)
from inventory.serializers import (
    CategorySerializer,
    MedicineSerializer
)
from inventory.models import (
    Category,
    Medicine
)


class CategoryListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class MedicineManagementAPIView(CreatedByMixin, generics.ListCreateAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()


class MedicineDetailedAPIView(CreatedByMixin, generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    lookup_field = 'id'

