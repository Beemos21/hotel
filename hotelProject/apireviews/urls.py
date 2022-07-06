# basic URL config.
from django.urls import include, path
# importing routers
from rest_framework import routers
from rest_framework.routers import DefaultRouter
# from api import viewset
# importing views
# from api import viewset
from .views import myReviewViewSet, allReviewViewSet
# other imports


# define the router
router = routers.DefaultRouter()
# define the router path and viewset to be used
router.register(r'myReview', myReviewViewSet, basename='myReviewapi')
router.register(r'allReview', allReviewViewSet, basename='allReviewapi')


# specify URL Path for rest_framework

urlpatterns = [
	path('', include(router.urls)),
]
