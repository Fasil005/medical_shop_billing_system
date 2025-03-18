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
