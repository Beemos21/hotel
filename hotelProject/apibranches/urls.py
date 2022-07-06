# basic URL config.
from django.urls import include, path
# importing routers
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

# define the router
router = routers.DefaultRouter()
# define the router path and viewset to be used
router.register(r'all-branches', GetBranchesViewSet, basename='all-branches-api')
router.register(r'available-room-types', AvalabilityView, basename='available-room-types-api')
router.register(r'all-room-types', GetAllRoomTypeView, basename='all-room-types-api')
router.register(r'room-type-detail', GetRoomTypeDetailView, basename='room-type-detail-api')
# specify URL Path for rest_framework

urlpatterns = [
    path('', include(router.urls)),
]
