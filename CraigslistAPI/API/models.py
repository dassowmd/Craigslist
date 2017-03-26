from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.
class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    Cl_Item_ID = models.CharField(max_length=1000)
    KeyParam = models.CharField(max_length=45)
    ValueParam = models.CharField(max_length=10000)
    ScrapedDateTime = models.CharField(max_length=45)
    RSS_Feed_String = models.CharField(max_length=1000)

    def __str__(self):
        s = str(self.KeyParam) + ":" + str(self.ValueParam)
        return s
