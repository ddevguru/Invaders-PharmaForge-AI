from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    PharmacistDashboard,
    VerifyPharmacist,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),

    path("pharmacist/dashboard/", PharmacistDashboard.as_view()),
    path("admin/verify-pharmacist/<int:user_id>/", VerifyPharmacist.as_view()),
]
