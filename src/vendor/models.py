from django.db import models

class MenuItem(models.Model):
    title = models.TextField()
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
