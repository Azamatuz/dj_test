from django.shortcuts import render, get_object_or_404

from .models import MenuItem


def menu_item_list_view(request):
    qs = MenuItem.objects.all()
    print(qs)
    template_name = 'menu/item_list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

def menu_item_create_view(request):
    template_name = 'menu/item_create.html'
    context = {'form':None}
    return render(request, template_name, context)

def menu_item_detail_view(request, slug):
    obj = get_object_or_404(MenuItem, slug=slug)
    template_name = 'menu/item_detail.html'
    context = {'object': obj}
    return render(request, template_name, context)

def menu_item_update_view(request, slug):
    obj = get_object_or_404(MenuItem, slug=slug)
    template_name = 'menu/item_update.html'
    context = {'object': obj, 'form':None}
    return render(request, template_name, context)

def menu_item_delete_view(request, slug):
    obj = get_object_or_404(MenuItem, slug=slug)
    template_name = 'menu/item_delete.html'
    context = {'object': obj,'form':None}
    return render(request, template_name, context)