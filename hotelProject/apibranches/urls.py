# basic URL config.
from django.urls import include, path
# importing routers
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import GetBranchesViewSet, GetRoomAvailabilityViewSet

# define the router
router = routers.DefaultRouter()
# define the router path and viewset to be used
router.register(r'allBranches', GetBranchesViewSet, basename='allBranchesapi')
router.register(r'getAvailableRooms', GetRoomAvailabilityViewSet, basename='getAvailableRooms')

# specify URL Path for rest_framework

urlpatterns = [
    path('', include(router.urls)),
]
