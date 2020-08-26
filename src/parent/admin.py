from django.contrib import admin

from .models import Address, Kid, OrderItem, Order

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street',
        'city',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street', 'city', 'zip']

admin.site.register(Address, AddressAdmin)
admin.site.register(Kid)
admin.site.register(Order)
admin.site.register(OrderItem)
