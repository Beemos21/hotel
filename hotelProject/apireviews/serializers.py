from rest_framework import serializers
# now import models from models.py
from booking.models import Review


# from django.apps import apps
# MyModel1 = apps.get_model('booking', 'Review')

# create a models serializer

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ('usr_id', 'comment', 'rate',)
