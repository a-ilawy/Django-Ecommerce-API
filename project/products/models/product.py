from django.contrib.auth import get_user_model
from django.db import models

from .base import *

User = get_user_model()


class Product(BaseModel):

    name = models.CharField(max_length=255, help_text="Name of the medication")
    factory = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True,default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, null=True, blank=True)
    stock  = models.IntegerField(default=0)
    code = models.CharField(max_length=255, null=True, blank=True)
    number_of_sales  = models.IntegerField(default=0)
    rating  = models.FloatField(default=0)
    number_of_ratings  = models.IntegerField(default=0)
    size = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    additional_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
    