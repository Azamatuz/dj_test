from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class MenuItem(models.Model): #menuitem_set -> queryset
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
