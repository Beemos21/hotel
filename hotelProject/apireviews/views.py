from rest_framework import viewsets

from .serializers import ReviewSerializer
from booking.models import Review

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

class myReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()  # mn ayy table badi jibon
    serializer_class = ReviewSerializer  # shu badu yesta3mel la ye2ra
    permission_classes = [IsAuthenticated]  # this will check if it is authenticated or not
    authentication_classes = [JWTAuthentication]  # this will handel authentication automatically

    def get_queryset(self):
        return Review.objects.all().filter(usr_id=self.request.user.pk).all()


class allReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()  # mn ayy table badi jibon
    serializer_class = ReviewSerializer  # shu badu yesta3mel la ye2ra
    