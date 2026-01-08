from rest_framework import serializers
from .models import User, CustomerProfile, PharmacistProfile, WarehouseProfile
from .firebase import verify_firebase_token


class RegisterSerializer(serializers.Serializer):
    firebase_token = serializers.CharField()
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    license_number = serializers.CharField(required=False)
    pharmacy_name = serializers.CharField(required=False)
    warehouse_id = serializers.CharField(required=False)

    def validate(self, data):
        phone = verify_firebase_token(data["firebase_token"])
        data["phone_number"] = phone

        if data["role"] == "PHARMACIST" and not data.get("license_number"):
            raise serializers.ValidationError("License number required")

        if data["role"] == "WAREHOUSE" and not data.get("warehouse_id"):
            raise serializers.ValidationError("Warehouse ID required")

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data["phone_number"],
            role=validated_data["role"]
        )

        if user.role == "CUSTOMER":
            CustomerProfile.objects.create(user=user)

        if user.role == "PHARMACIST":
            PharmacistProfile.objects.create(
                user=user,
                license_number=validated_data["license_number"],
                pharmacy_name=validated_data["pharmacy_name"]
            )

        if user.role == "WAREHOUSE":
            WarehouseProfile.objects.create(
                user=user,
                warehouse_id=validated_data["warehouse_id"]
            )

        return user
