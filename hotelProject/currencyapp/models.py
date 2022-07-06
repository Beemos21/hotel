import datetime
from django.db import models



class Currency(models.Model):
    name = models.CharField(max_length=50)
    symbole = models.CharField(max_length=4)

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    def __str__(self):
        return self.name