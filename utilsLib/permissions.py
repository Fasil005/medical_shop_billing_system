from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    """Allows access only to Admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_role()

class InventoryManagerPermission(BasePermission):
    """Allows access only to Inventory Managers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_inventory_manager_role()

class StaffPermission(BasePermission):
    """Allows access only to Staff users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff_role()
