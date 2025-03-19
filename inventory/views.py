from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from inventory.mixins import CreatedByMixin
from utilsLib.permissions import (
    InventoryManagerPermission,
    AdminPermission,
    StaffReadOnlyPermission,
    StaffFullAccessPermission,
    StaffWriteOnlyPermission
)
from inventory.serializers import (
    CategorySerializer,
    MedicineSerializer,
    StockSerializer,
    MedicinePackageSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    SupplierSerializer
)
from inventory.models import (
    Category,
    Medicine,
    MedicineStock,
    MedicinePackaging,
    Invoice,
    Supplier
)


class CategoryListAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class MedicineManagementAPIView(CreatedByMixin, generics.ListCreateAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission | StaffReadOnlyPermission]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()


class MedicineDetailedManagementAPIView(CreatedByMixin, generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission | StaffReadOnlyPermission]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    lookup_field = 'id'


class MedicinePackageManagementAPIView(CreatedByMixin, generics.ListCreateAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission]
    serializer_class = MedicinePackageSerializer
    queryset = MedicinePackaging.objects.all()


class MedicinePackageDetailedManagementAPIView(CreatedByMixin, generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission]
    serializer_class = MedicinePackageSerializer
    queryset = MedicinePackaging.objects.all()
    lookup_field= 'id'


class SupplierManagementAPIView(generics.ListCreateAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


class SupplierDetailedManagementAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    lookup_field = 'id'


class StockManagementAPIView(CreatedByMixin, generics.ListCreateAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission | StaffReadOnlyPermission]
    serializer_class = StockSerializer
    queryset = MedicineStock.objects.all()
    ordering_fields = '__all__'


class StockDetailedManagementAPIView(CreatedByMixin, generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [InventoryManagerPermission | AdminPermission]
    serializer_class = StockSerializer
    queryset = MedicineStock.objects.all()
    lookup_field = 'id'


class InvoiceManagementAPIView(generics.ListCreateAPIView):

    permission_classes = [StaffWriteOnlyPermission | AdminPermission]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    