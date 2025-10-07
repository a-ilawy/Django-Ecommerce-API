from django.db import models
from .user import User  

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')

    def __str__(self):
        return self.user.full_name