from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"


class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "PHARMACIST"


class IsWarehouse(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "WAREHOUSE"


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "CUSTOMER"
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"


class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "PHARMACIST"


class IsWarehouse(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "WAREHOUSE"


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "CUSTOMER"
