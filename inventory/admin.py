from django.contrib import admin

from inventory.models import (
    Category,
    Medicine,
    Invoice,
    InvoiceItem
)

admin.site.register(Category)
admin.site.register(Medicine)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
