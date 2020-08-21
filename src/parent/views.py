from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import OrderItem, Order
from vendor.models import MenuItem

from.forms import KidModelForm
from .models import Kid


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
            messages.info(request, "Quantity of " + item.title + " was updated.")
            return redirect('/menu/')
        else:
            order.items.add(order_item)
            messages.info(request, item.title +" was added to your cart.")
            return redirect('/menu/')
    else:
        event_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            event_date=event_date
            )
        order.items.add(order_item)
        messages.info(request, item.title +" was added to your cart.")
        return redirect('/menu/')


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
            messages.info(request, item.title +" was removed from your cart.")
            return redirect('/menu/')

        else:
            messages.info(request, item.title +" was not in your cart.")
            return redirect('/menu/')
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('/menu/')


def kid_list_view(request):
    if request.user.is_parent:
        qs = Kid.objects.filter(user=request.user)
    elif request.user.is_school:
        qs = Kid.objects.all()
    template_name = 'children/kid_list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

#@login_required(login_url='/signin')
@login_required
def kid_create_view(request):
    form = KidModelForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.slug = str(obj.user) + '_' + form.cleaned_data.get('first_name') 
        obj.save()
        return redirect('/children/')
        
    template_name = 'children/form.html'
    context = {'form':form}
    return render(request, template_name, context)


def kid_detail_view(request, slug):
    obj = get_object_or_404(Kid, slug=slug)
    template_name = 'children/kid_detail.html'
    context = {'object': obj}
    return render(request, template_name, context)

@login_required
def kid_update_view(request, slug):
    obj = get_object_or_404(Kid, slug=slug)
    form = KidModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/children/')
    template_name = 'children/form.html'
    context = {'title':f'Update {obj.first_name}','form': form}
    return render(request, template_name, context)

@login_required
def kid_delete_view(request, slug):
    obj = get_object_or_404(Kid, slug=slug)
    template_name = 'children/kid_delete.html'
    if request.method == 'POST':
        obj.delete()
        return redirect('/children')
    context = {'object': obj}
    return render(request, template_name, context)

