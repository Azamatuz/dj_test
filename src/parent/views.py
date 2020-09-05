from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .models import Address, OrderItem, Order
from vendor.models import MenuItem

from.forms import KidModelForm, CheckoutForm
from .models import Kid

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            template_name = 'order/checkout.html'
            context = {
                'form': form,
                'order': order
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, template_name, context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have any active order')
            return redirect('/order-summary/')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('parent:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_street = form.cleaned_data.get(
                        'shipping_street')
                    shipping_city = form.cleaned_data.get(
                        'shipping_city')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_province = form.cleaned_data.get(
                        'shipping_province')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_street, shipping_city, shipping_country, shipping_province, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street=shipping_street,
                            city=shipping_city,
                            country=shipping_country,
                            province=shipping_province,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('parent:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_street = form.cleaned_data.get(
                        'billing_street')
                    billing_city = form.cleaned_data.get(
                        'billing_city')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_province = form.cleaned_data.get(
                        'billing_province')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_street, billing_city, billing_country, billing_province, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street=billing_street,
                            city=billing_city,
                            country=billing_country,
                            province=billing_province,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('parent:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('parent:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('parent:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("parent:order-summary")


    #         order = Order.objects.get(user=self.request.user, ordered=False)
    #         if form.is_valid():
    #             street = form.cleaned_data.get('street')
    #             city = form.cleaned_data.get('city')
    #             country = form.cleaned_data.get('country')
    #             province = form.cleaned_data.get('province')
    #             zip = form.cleaned_data.get('zip')
                
    #             payment_option = form.cleaned_data.get('payment_option')
    #             billing_address =  (
    #                 user=self.request.user,
    #                 street=street,
    #                 city=city,
    #                 country=country,Address
    #                 province=province,
    #                 zip=zip
    #             )
    #             billing_address.save()
    #             order.billing_address = billing_address
    #             order.save()
                             
    #             return redirect('parent:checkout')
    #         messages.warning(self.request, 'Failed checkout')
    #         return redirect('parent:checkout')
    #     except ObjectDoesNotExist:
    #         messages.warning(self.request, 'You do not have any active order')
    #         return redirect('/order-summary/')
        
    # #return redirect("parent:order-summary")


@login_required
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
            return redirect('/order-summary/')
        else:
            order.items.add(order_item)
            messages.info(request, item.title +" was added to your cart.")
            return redirect('/order-summary/')
    else:
        event_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            event_date=event_date
            )
        order.items.add(order_item)
        messages.info(request, item.title +" was added to your cart.")
        return redirect('/order-summary/')

@login_required
def remove_from_cart(request, slug):#remove product item from the cart
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

def remove_item_from_cart(request, slug): #remove single item from the cart
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, 'Quantity of ' + item.title +" was updated.")
            return redirect('/order-summary/')

        else:
            messages.info(request, item.title +" was not in your cart.")
            return redirect('/menu/')
    else:
        messages.info(request, "You do not have an active order.")
        return redirect('/menu/')


def kid_list_view(request):
    if request.user.is_parent:
        qs = Kid.objects.filter(user=request.user)
    else:
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

