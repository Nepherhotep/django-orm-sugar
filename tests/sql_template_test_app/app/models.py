from django.db import models


# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    birthday_date = models.DateField(null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
