from django.conf import settings
from django.db import models
from django.shortcuts import reverse

User = settings.AUTH_USER_MODEL

CATEGORY_CHOICES = (
    ('M', 'Main meal'),
    ('D', 'Drink'),
    ('S', 'Snack')
)

LABEl_CHOICES = (
    ('-', 'None'),
    ('P', 'Pork'),
    ('V', 'Veggie'),
    ('N', 'Nuts')
)
class MenuItem(models.Model): #menuitem_set -> queryset
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1, default='M')
    label = models.CharField(choices=LABEl_CHOICES, max_length=1, default='-') 


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/menu/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
    
    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    
    def get_create_url(self):
        return "/menu-new/"

    def get_add_to_cart_url(self):
        return f'/order/add-to-cart/{self.slug}'
        
    def get_remove_from_cart_url(self):
        return f'/order/remove-from-cart/{self.slug}'

