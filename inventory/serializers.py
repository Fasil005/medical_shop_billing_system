from rest_framework import serializers

from users.serializers import UserSerializer
from inventory.tasks import process_invoice
from inventory.models import (
    Category,
    Medicine,
    MedicineStock,
    MedicinePackaging,
    Invoice,
    InvoiceItem,
    Supplier
)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    
class MedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine
        fields = '__all__'


class MedicinePackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicinePackaging
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicineStock
        fields = '__all__'

class DashboardStockSerializer(serializers.ModelSerializer):

    created_by = UserSerializer()
    medicine = MedicineSerializer()
    packaging = MedicinePackageSerializer()

    class Meta:
        model = MedicineStock
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    packaging_type = serializers.ChoiceField(choices=MedicinePackaging.PACKAGING_CHOICES, write_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['medicine', 'packaging_type', 'quantity', 'price', 'total_price']

    def validate(self, data):
        """Override validation to fetch price from MedicinePackaging."""

        medicine_id = data.get('medicine').id
        packaging_type = data.pop('packaging_type')

        try:
            medicine = Medicine.objects.get(id=medicine_id)
            packaging = medicine.packaging.filter(packaging_type=packaging_type).first()
            if not packaging:
                raise serializers.ValidationError(f"Invalid packaging type: {packaging_type}")

            data['price'] = packaging.price_per_package
            data['total_price'] = data['price'] * data['quantity']

        except Medicine.DoesNotExist:
            raise serializers.ValidationError(f"Medicine ID {medicine_id} not found")

        return data

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'customer_name', 'customer_email', 'total_price', 'created_by', 'items']

    def validate(self, data):
        """Override validate() to calculate total invoice price."""

        items_data = data.get('items', [])
        total_invoice_price = sum(item['total_price'] for item in items_data)
        data['total_price'] = total_invoice_price
        return data

    def create(self, validated_data):
        """Create invoice and items in a single transaction."""

        validated_data['created_by'] = request = self.context.get("request").user
        items_data = validated_data.pop('items')
        print(validated_data)
        invoice = Invoice.objects.create(**validated_data)

        invoice_items = [
            InvoiceItem(invoice=invoice, **item) for item in items_data
        ]

        InvoiceItem.objects.bulk_create(invoice_items)
        
        process_invoice.delay(invoice.id)

        return invoice
    

class StaffSalesReportSerializer(serializers.Serializer):

    staff_id = serializers.IntegerField()
    staff_name = serializers.CharField()
    total_amount_billed = serializers.IntegerField()
    total_medicines_sold = serializers.IntegerField()
    total_invoice_generated = serializers.IntegerField()


class SalesReportSerializer(serializers.Serializer):
    """Serializer for formatted sales report response"""
    
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total_billed_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_sold_medicines = serializers.IntegerField()
    total_stocks_available_medicine_count = serializers.IntegerField()