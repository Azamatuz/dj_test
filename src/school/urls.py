from django.urls import path

from .views import(
    event_item_detail_view,
    event_item_list_view,
    event_item_create_view,
    event_item_update_view,
    event_item_delete_view,
)

urlpatterns = [

    path('', event_item_list_view),
    path('<str:slug>/', event_item_detail_view),
    path('<str:slug>/edit/', event_item_update_view),
    path('<str:slug>/delete/', event_item_delete_view),
]
