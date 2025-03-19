from django.contrib import admin

from inventory.models import (
    Category,
    Medicine,
    Invoice,
    InvoiceItem,
    MedicinePackaging,
    MedicineStock
)

admin.site.register(Category)
admin.site.register(Medicine)
admin.site.register(MedicinePackaging)
admin.site.register(MedicineStock)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
