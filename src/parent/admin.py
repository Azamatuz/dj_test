from django.contrib import admin

from .models import Kid, OrderItem, Order

admin.site.register(Kid)
admin.site.register(Order)
admin.site.register(OrderItem)
