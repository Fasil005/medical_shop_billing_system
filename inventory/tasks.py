from datetime import timedelta

from django.db.models import F, ExpressionWrapper, fields
from django.utils.timezone import now
from django.db import models

from celery import shared_task

from inventory.models import Invoice, MedicineStock
from users.models import User
from inventory.utils import get_email_message, update_stock
from utilsLib.models import Notification
from utilsLib.email import EmailService 

@shared_task
def process_invoice(invoice_id):
    """Handles invoice email notification, stock update, and notification creation asynchronously."""
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        user = invoice.created_by

        update_stock(invoice, user)

        subject = f"Invoice Created - #{invoice.id}"
        message = get_email_message(invoice)
        recipient_list = [invoice.customer_email]
        
        EmailService.send_html_email(subject, message, recipient_list)


        Notification.objects.create(
            user=user,
            message=f"Invoice #{invoice.id} created successfully. Total: ₹{invoice.total_price}",
            timestamp=now()
        )

        return f"Invoice {invoice.id} processed successfully."

    except Invoice.DoesNotExist:
        return f"Invoice {invoice_id} not found."
    


@shared_task
def stock_replenishment_reminders():
    """Check for low-stock medicines and notify admins."""

    current_date = now().date()
    medicines = MedicineStock.objects.annotate(
            expiry_alert_date=ExpressionWrapper(
                F("expiry_date") - ExpressionWrapper(F("expiry_alert_level")  * timedelta(days=1), output_field=fields.DurationField()),
                output_field=fields.DateField()
            )
        ).filter(
            models.Q(stock__lte=F("alert_level")) |
            models.Q(expiry_alert_date__lte=current_date) 
        ).select_related("medicine")

    if medicines.exists():
        users = list(User.objects.filter(role__in=[User.Role.INVENTORY_MANAGER, User.Role.ADMIN]))

        notifications = []

        for stock in medicines:
            if stock.stock <= stock.alert_level:
                if stock.supplier:
                    message = f"Stock Alert: {stock.medicine.name} is low (Only {stock.stock} left). Contact {stock.supplier.name} ({stock.supplier.phone_number})."
                else:
                    message = f"Stock Alert: {stock.medicine.name} stock is low (Only {stock.stock} left). No supplier linked!"

                for user in users:
                    notifications.append(Notification(user=user, message=message, timestamp=now()))

            if stock.expiry_alert_date.date() <= current_date:
                days_left = (stock.expiry_date - current_date).days
                message = f"Expiry Alert: {stock.medicine.name} (Batch {stock.id}) expires in {days_left} days!"
                for user in users:
                    notifications.append(Notification(user=user, message=message, timestamp=now()))

        if notifications:
            Notification.objects.bulk_create(notifications)

    return "Stock check completed."

