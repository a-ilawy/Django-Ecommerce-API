from django.contrib.auth import get_user_model  
from django.db import models
from .base import *

User = get_user_model()

class Brand(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="brand_images", null=True, blank=True)

    def __str__(self):
        return self.name
    