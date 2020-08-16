from django.conf import settings
from django.db import models

from vendor.models import MenuItem

User = settings.AUTH_USER_MODEL

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}' 
    
    def get_add_to_cart_url(self):
        return reverse('parent:add_to_cart', kwargs={
            'slug':self.slug
        })

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)



