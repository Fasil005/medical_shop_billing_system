from django.utils.timezone import now

from inventory.models import MedicineStock
from utilsLib.models import Notification


def update_stock(invoice, user):

    for item in invoice.items.all():
        quantity_needed = item.quantity
        medicine = item.medicine

        stock_entries = MedicineStock.objects.filter(
                medicine=medicine, stock__gt=0
            )
        
        for stock in stock_entries:
            if quantity_needed <= 0:
                break  

            if stock.stock >= quantity_needed:
                
                stock.stock -= quantity_needed
                stock.save(update_fields=["stock"])
                quantity_needed = 0
            else:
                quantity_needed -= stock.stock
                stock.stock = 0
                stock.save(update_fields=["stock"])
        
            if stock.stock <= stock.alert_level:
                Notification.objects.create(
                    user=user,
                    message=f"Stock for {medicine.name} is low ({stock.stock} left).",
                    timestamp=now()
                )


def get_email_message(invoice):

    invoice_items = invoice.items.all()

    item_details = "\n".join([
        f"{item.medicine.name} - {item.quantity} x ₹{item.price} = ₹{item.total_price}"
        for item in invoice_items
    ])

    total_amount = f"Total Amount: ₹{invoice.total_price}"

    message = f"""
        Dear Customer,

        Thank you for your purchase! Your invoice details are as follows:

        Invoice ID: {invoice.id}
        Date: {invoice.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        
        Items Purchased:
        {item_details}

        {total_amount}

        If you have any questions, feel free to contact us.

        Regards
        """
    
    return message