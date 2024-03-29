from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

from.forms import MenuItemModelForm
from .models import MenuItem


def menu_item_list_view(request):
    if request.user.is_vendor:
        qs = MenuItem.objects.filter(user=request.user)
    else:
        qs = MenuItem.objects.all()
    template_name = 'menu/item_list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

#@login_required(login_url='/signin')
@login_required
def menu_item_create_view(request):
    form = MenuItemModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.slug = str(obj.user) + '_' + form.cleaned_data.get('title') 
        obj.save()
        return redirect('/menu')
        
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
        return redirect('/menu/'+slug)
    template_name = 'menu/form.html'
    context = {'title':f'Update {obj.title}','form': form}
    return render(request, template_name, context)

@login_required
def menu_item_delete_view(request, slug):
    obj = get_object_or_404(MenuItem, slug=slug)
    template_name = 'menu/item_delete.html'
    if request.method == 'POST':
        obj.delete()
        return redirect('/menu')
    context = {'object': obj}
    return render(request, template_name, context)