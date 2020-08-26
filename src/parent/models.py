from django.conf import settings
from django.db import models

from vendor.models import MenuItem

User = settings.AUTH_USER_MODEL

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

COUNTRY_CHOICES = (
    ('CA', 'Canada'),
    #('US', 'United States')
)

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

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'Addresses'

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
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   # kid = models.ForeignKey(Kid, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user.email
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price() #order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total






