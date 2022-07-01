from rest_framework import serializers
# now import models from models.py
from roomManager.models import HotelInfo, RoomType
from datetime import datetime
from django.db import connection


# create a models serializer

class BranchesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HotelInfo
        fields = ('name', 'city',)


class AvailableRoomsSerializer(serializers.Serializer):
    # model = RoomType
    """
    Serializer for available rooms endpoint.
    """
    fromdate = serializers.DateField(required=True)
    todate = serializers.DateField(required=True)
    hotelid = serializers.IntegerField()
    nbadult = serializers.IntegerField(required=True)
    nbchildren = serializers.IntegerField()
    nbrooms = serializers.IntegerField()

    # class Meta:
    #     model = RoomType
    #     fields = ('room_type', 'fromdate', 'todate', 'hotelid', 'nbadult', 'nbchildren', 'nbrooms',)
    # extra_kwargs = {
    #     'fromdate': {'required': True},
    #     'todate': {'required': True},
    #     'hotelid': {'required': False},
    #     'nbadult': {'required': True},
    #     'nbchildren': {'required': False},
    #     'nbrooms': {'required': False},
    # }
