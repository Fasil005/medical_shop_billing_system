from django.db.models import Sum, Count, F, Min, Max

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
    SupplierSerializer,
    StaffSalesReportSerializer,
    SalesReportSerializer
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
    filterset_fields  = ["created_by",]

class StaffSalesReportAPIView(generics.ListAPIView):

    permission_classes = [AdminPermission]
    serializer_class = StaffSalesReportSerializer
    filterset_fields  = ["created_by",]

    def get_queryset(self, ):
        queryset = (Invoice.objects.values("created_by")
            .filter(created_by__isnull=False).annotate(
                staff_id=F("created_by"),
                staff_name=F("created_by__first_name"),
                total_amount_billed=Sum("total_price"),
                total_invoice_generated=Count("id", distinct=True),
                total_medicines_sold=Sum("items__quantity"),
            )
        )

        return queryset


class DashboardMetricsAPIView(generics.ListAPIView):

    permission_classes = [AdminPermission]
    serializer_class = SalesReportSerializer

    def get_queryset(self):
        """Return filtered queryset for sales reports."""

        queryset = Invoice.objects.exclude(created_by__isnull=True) 

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

        return queryset

    def list(self, request, *args, **kwargs):
        """Override list method to return aggregated data as response."""
        queryset = self.get_queryset() 

        # Perform aggregation separately inside list()
        report_data = queryset.aggregate(
            start_date=Min("created_at"),
            end_date=Max("created_at"),
            total_billed_amount=Sum("total_price", default=0),
            total_sold_medicines=Sum("items__quantity", default=0),
        )

        report_data["total_stocks_available_medicine_count"] = MedicineStock.objects.count()

        return Response(report_data)


