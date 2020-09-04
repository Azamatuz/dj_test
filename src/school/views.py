from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

from.forms import EventItemModelForm
from .models import EventItem

from vendor.models import MenuItem


def event_item_list_view(request):
    if request.user.is_school:
        qs = EventItem.objects.filter(user=request.user)
    elif request.user.is_parent:
        qs = EventItem.objects.all()
    template_name = 'event/event_list.html'
    context = {'object_list': qs}
    return render(request, template_name, context)

#@login_required(login_url='/signin')
@login_required

def event_item_create_view(request):
    form = EventItemModelForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.slug = str(obj.user) + '_' + form.cleaned_data.get('title') 
        obj.save()
        return redirect('/event')
        
    template_name = 'event/form.html'
    context = {'form':form}
    return render(request, template_name, context)


def event_item_detail_view(request, slug):
    obj = get_object_or_404(EventItem, slug=slug)
    template_name = 'event/event_detail.html'
    context = {'object': obj}
    return render(request, template_name, context)

@login_required
#@user_is_event_author
def event_item_update_view(request, slug):
    obj = get_object_or_404(EventItem, slug=slug)
    form = EventItemModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/event/'+slug)
    template_name = 'event/form.html'
    context = {'title':f'Update {obj.title}','form': form}
    return render(request, template_name, context)

@login_required
#@user_is_event_author
def event_item_delete_view(request, slug):
    obj = get_object_or_404(EventItem, slug=slug)
    template_name = 'event/event_delete.html'
    if request.method == 'POST':
        obj.delete()
        return redirect('/event')
    context = {'object': obj}
    return render(request, template_name, context)


# def user_menu_item_list_view():
#     qs = MenuItem.objects.filter(user=request.user)
#     template_name = 'event/event_list.html'
#     context = {'object_list': qs}
#     return render(request, template_name, context)