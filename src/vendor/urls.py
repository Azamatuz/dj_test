from django.urls import path

from .views import(
    menu_item_detail_view,
    menu_item_list_view,
    menu_item_update_view,
    menu_item_delete_view
)

app_name = 'vendor'
urlpatterns = [

    path('', menu_item_list_view, name='menulist'),
    path('<str:slug>/', menu_item_detail_view, name='menuitem'),
    path('<str:slug>/edit/', menu_item_update_view),
    path('<str:slug>/delete/', menu_item_delete_view),
]
