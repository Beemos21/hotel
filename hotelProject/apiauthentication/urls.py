from django.urls import path
from .views import RegisterUserAPIView, ChangePasswordView, LogoutAPIView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('register', RegisterUserAPIView.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='get_token'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    # path('logoutAll', LogoutAllView.as_view(), name='auth_logout_all'),
    path('changePassword', ChangePasswordView.as_view(), name='change_password'),
    path('profile', ProfileView.as_view(), name='profile'),

    path('refreshToken', TokenRefreshView.as_view(), name='refresh_token'),
    path('verifyToken', TokenVerifyView.as_view(), name='verify_token'),
]
