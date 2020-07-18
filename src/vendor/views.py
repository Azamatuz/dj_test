from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

from.forms import MenuItemModelForm
from .models import MenuItem


def menu_item_list_view(request):
    qs = MenuItem.objects.all()
    print(qs)
    template_name = 'menu/item_list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

#@login_required(login_url='/signin')
@login_required
def menu_item_create_view(request):
    form = MenuItemModelForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.slug = str(obj.user) + '_' + form.cleaned_data.get('title') 
        obj.save()
        form = MenuItemModelForm()
    template_name = 'menu/form.html'
    context = {'form':form}
    return render(request, template_name, context)


def menu_item_detail_view(request, slug):
    obj = get_object_or_404(MenuItem, slug=slug)
    template_name = 'menu/item_detail.html'
    context = {'object': obj}
    return render(request, template_name, context)

@login_required
def menu_item_update_view(request, slug):
    obj = get_object_or_404(MenuItem, slug=slug)
    form = MenuItemModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'menu/form.html'
    context = {'title':f'Update {obj.title}','form': form}
    return render(request, template_name, context)

@login_required
def menu_item_delete_view(request, slug):
    obj = get_object_or_404(MenuItem, slug=slug)
    template_name = 'menu/item_delete.html'
    if request.method == 'POST':
        obj.delete()
    context = {'object': obj}
    return render(request, template_name, context)