from django.utils import timezone
from django.db import models

from users.models import User


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):

    name = models.CharField(max_length=255, unique=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_medicines")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="medicines")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.company_name}) - {self.name} - {self.category}"


class MedicinePackaging(models.Model):
    """Stores different packaging types for a medicine (e.g., Strip, Pack, Box)."""

    PACKAGING_CHOICES = [
        ('single', 'Single Piece'),
        ('strip', 'Strip'),
        ('pack', 'Pack'),
        ('box', 'Box'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="packaging")
    packaging_type = models.CharField(max_length=10, choices=PACKAGING_CHOICES)
    units_per_package = models.PositiveIntegerField()  # How many base units (e.g., 1 strip = 10 tablets)
    price_per_package = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} - {self.packaging_type} ({self.units_per_package})"
    

class Supplier(models.Model):

    name = models.CharField(max_length=255, unique=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    medicines_supplied = models.ManyToManyField("Medicine", related_name="suppliers")

    def __str__(self):
        return self.name



class MedicineStock(models.Model):
    
    stock = models.PositiveIntegerField()
    expiry_date = models.DateField()

    alert_level = models.IntegerField()
    expiry_alert_level = models.IntegerField(
        default=15,
        help_text="Number of days before expiry to trigger an alert. Example: 30 means you'll get a reminder 30 days before expiry."
        )

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_supplies")
    packaging = models.ForeignKey(MedicinePackaging, on_delete=models.CASCADE, related_name="stocks")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="stock_updates")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="medicines_stocks")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-expiry_date",)

    def is_expired(self):
        """Check if the medicine is expired."""
        return self.expiry_date < timezone.now().date()

    def __str__(self):
        return f"{self.packaging} - {self.medicine}"
    

class Invoice(models.Model):
    """Stores invoices for customer purchases."""
    
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="bills")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Invoice {self.id} - {self.total_price}"


class InvoiceItem(models.Model):
    """Stores individual medicines in an invoice."""
    
    
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Auto-calculate total price before saving"""
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity} = {self.total_price}"