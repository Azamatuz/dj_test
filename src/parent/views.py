from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import OrderItem, Order
from vendor.models import MenuItem



def add_to_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('/menu/'+slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('/menu/'+slug)
    else:
        event_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            event_date=event_date
            )
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('/menu/'+slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user, 
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect('/menu/'+slug)

        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('/menu/'+slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('/menu/'+slug)

