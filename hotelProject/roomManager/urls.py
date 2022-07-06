from django.urls import path
from .views import getview
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.http import HttpResponse,HttpRequest

urlpatterns = [
    path('roomavailability', getview, name='roomavailability'),

]
