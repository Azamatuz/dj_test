from django.urls import path

from .views import(
    menu_item_detail_view,
    menu_item_list_view,
    menu_item_create_view,
    menu_item_update_view,
    menu_item_delete_view,
)

urlpatterns = [

    path('', menu_item_list_view),
    path('<str:slug>/', menu_item_detail_view),
    path('<str:slug>/edit/', menu_item_update_view),
    path('<str:slug>/delete/', menu_item_delete_view),
]
