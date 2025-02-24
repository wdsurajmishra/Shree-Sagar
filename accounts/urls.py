from django.urls import path
from .views import LoginView, SendOTPView, ProfileView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='my_profile'),
]