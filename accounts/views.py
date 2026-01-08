from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer
from .models import User, PharmacistProfile
from .firebase import verify_firebase_token
from .permissions import IsAdmin, IsPharmacist


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Registered successfully"})


class LoginView(APIView):
    def post(self, request):
        phone = verify_firebase_token(request.data["firebase_token"])
        user = User.objects.get(phone_number=phone)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "role": user.role
        })


# 🔒 PHARMACIST-ONLY ENDPOINT
class PharmacistDashboard(APIView):
    permission_classes = [IsAuthenticated, IsPharmacist]

    def get(self, request):
        return Response({"message": "Pharmacist dashboard"})


# 🔒 ADMIN-ONLY ENDPOINT
class VerifyPharmacist(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        profile = PharmacistProfile.objects.get(user_id=user_id)
        profile.is_verified = True
        profile.save()
        return Response({"message": "Pharmacist verified"})
