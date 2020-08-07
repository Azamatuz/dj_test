from django.core.exceptions import PermissionDenied
from .models import EventItem

def user_is_event_author(function):
    def wrap(request, *args, **kwargs):
        event = EventItem.objects.get(slug=kwargs['slug'])
        if event.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap