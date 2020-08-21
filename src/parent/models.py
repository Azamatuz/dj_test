from django.conf import settings
from django.db import models

from vendor.models import MenuItem

User = settings.AUTH_USER_MODEL

PROVINCE_CHOICES = (
    ('AB', 'Alberta'), 
    ('BC', 'British Columbia'), 
    ('MB', 'Manitoba'), 
    ('NB', 'New Brunswick'), 
    ('NL', 'Newfoundland and Labrador'), 
    ('NT', 'Northwest Territories'), 
    ('NS', 'Nova Scotia'), 
    ('NU', 'Nunavut'), 
    ('ON', 'Ontario'), 
    ('PE', 'Prince Edward Island'), 
    ('QC', 'Quebec'), 
    ('SK', 'Saskatchewan'), 
    ('YT', 'Yukon')
    )

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}' 
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


class Kid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name =  models.CharField(max_length=120)
    slug = slug = models.SlugField(unique=True)
    last_name =  models.CharField(max_length=120)
    province = models.CharField(choices=PROVINCE_CHOICES, max_length=2, default='AB')
    city = models.CharField(max_length=120)
    school =  models.CharField(max_length=120)
    grade = models.CharField(max_length=120)
    teacher = models.CharField(max_length=120)

    def __str__(self):  
        return self.first_name
    
    def get_absolute_url(self):
        return f"/children/{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"
    
    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
    
    def get_create_url(self):
        return "/children-new/"


