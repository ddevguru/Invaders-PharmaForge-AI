from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, role):
        user = self.model(phone_number=phone_number, role=role)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, phone_number):
        user = self.create_user(phone_number, "ADMIN")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("CUSTOMER", "Customer"),
        ("WAREHOUSE", "Warehouse"),
        ("PHARMACIST", "Pharmacist"),
        ("ADMIN", "Admin"),
    )

    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.phone_number} ({self.role})"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class WarehouseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    warehouse_id = models.CharField(max_length=100)


class PharmacistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    pharmacy_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
