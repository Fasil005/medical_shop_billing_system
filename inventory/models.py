from django.utils import timezone
from django.db import models

from users.models import User


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Medicine(models.Model):

    name = models.CharField(max_length=255, unique=True)
    medicine_id = models.CharField(max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_medicines")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="medicines")



class MedicineStock(models.Model):
    
    PACKAGING_CHOICES = [
        ('single', 'Single Piece'),
        ('strip', 'Strip'),
        ('pack', 'Pack'),
        ('box', 'Box'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="stocks")
    packaging_type = models.CharField(max_length=10, choices=PACKAGING_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="stock_updates")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        """Check if the medicine is expired."""
        return self.expiry_date < timezone.now().date()

    def __str__(self):
        return f"{self.name} ({self.packaging_type}) - {self.price}"
    

class Invoice(models.Model):
    """Stores invoices for customer purchases."""
    
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bills")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.uid} - {self.total_price}"


class InvoiceItem(models.Model):
    """Stores individual medicines in an invoice."""
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """Auto-calculate total price before saving"""
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity} = {self.total_price}"