from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        INVENTORY_MANAGER = "inventory_manager", "Inventory Manager"
        STAFF = "staff", "Staff"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF
    )

    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def is_inventory_manager_role(self):
        return self.role == self.Role.INVENTORY_MANAGER

    def is_staff_role(self):
        return self.role == self.Role.STAFF
    
    def save(self, *args, **kwargs):
        """Ensure role and is_superuser stay in sync."""
        
        if self.role == self.Role.ADMIN:
            self.is_superuser = True
        elif self.is_superuser:
            self.role = self.Role.ADMIN
        else:
            self.is_superuser = False

        super().save(*args, **kwargs)
