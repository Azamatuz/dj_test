from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.email
    

class SchoolProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_full_name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.title

class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_full_name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.title