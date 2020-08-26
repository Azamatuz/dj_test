from django.urls import path
from .views import(
    add_to_cart,
    remove_from_cart,
    remove_item_from_cart,
    CheckoutView,
) 


app_name = 'parent'

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<str:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<str:slug>/', remove_item_from_cart, name='remove-item-from-cart'),

]
