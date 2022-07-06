from rest_framework import serializers
# now import models from models.py
from roomManager.models import HotelInfo, RoomType
from datetime import datetime
from django.db import connection

from rest_framework import serializers


class BranchesSerializer(serializers.HyperlinkedModelSerializer):
   city = serializers.CharField(source='city.city_name', read_only=True)
   city_ar = serializers.CharField(source='city.city_name_ar', read_only=True)

   class Meta:
      model = HotelInfo
      fields = ('id', 'name', 'name_ar', 'city', 'city_ar',)

class RoomTypeSerializer(serializers.HyperlinkedModelSerializer):

   symbole = serializers.CharField(source='currency.symbole', read_only=True)
   class Meta:
      model = RoomType
      fields = ('id','type_name','type_name_ar','price_per_day', 'description','description_ar','area','bedType','bedType_ar','special_features','special_features_ar','cover_image','symbole')


class AvalabilitySerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   id = serializers.IntegerField()
   capacity = serializers.IntegerField()
   type_name = serializers.CharField()
   type_name_ar = serializers.CharField()
   price_per_day = serializers.DecimalField(max_digits=10, decimal_places=3)
   countofroom = serializers.IntegerField()
   description = serializers.CharField()
   description_ar = serializers.CharField()
   area = serializers.IntegerField()
   bedType = serializers.CharField()
   bedType_ar = serializers.CharField()
   special_features = serializers.CharField()
   special_features_ar = serializers.CharField()
   cover_image=serializers.CharField()
   symbole=serializers.CharField()


class RoomTypeDetailSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   id = serializers.IntegerField()
   capacity = serializers.IntegerField()
   type_name = serializers.CharField()
   type_name_ar = serializers.CharField()
   price_per_day = serializers.DecimalField(max_digits=10, decimal_places=3)
   description = serializers.CharField()
   description_ar = serializers.CharField()
   area = serializers.IntegerField()
   bedType = serializers.CharField()
   bedType_ar = serializers.CharField()
   special_features = serializers.CharField()
   special_features_ar = serializers.CharField()
   cover_image=serializers.CharField()

   images = serializers.ListField()
   services = serializers.ListField()


