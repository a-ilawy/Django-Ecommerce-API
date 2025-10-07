from django.db import models
from .user import User

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True, default='Administrator')

    def __str__(self):
        return self.user.full_name