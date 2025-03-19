from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
    """Allows access only to Admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_role()

class InventoryManagerPermission(BasePermission):
    """Allows access only to Inventory Managers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_inventory_manager_role()

class StaffReadOnlyPermission(BasePermission):
    """Allows access only to Staff users for GET requests (Read-Only)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff_role() and request.method in ["GET"]

class StaffWriteOnlyPermission(BasePermission):
    """Allows access only to Staff users for POST requests (Write-Only)."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff_role() and request.method in ["POST"]

class StaffFullAccessPermission(BasePermission):
    """Allows full access (GET, POST, PUT, DELETE) to Staff users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff_role()
