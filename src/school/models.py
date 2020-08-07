from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Vendor(models.Model):
    email = models.CharField(max_length=200)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.email}'
    

class EventItem(models.Model): 
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(help_text="format (yyyy-mm-dd)")
    description = models.TextField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, default=1, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return f"/event/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
    
    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    
    def get_create_url(self):
        return "/event-new/"