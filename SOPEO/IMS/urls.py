from django.urls import path
from . import views


urlpatterns = [

  
    path("", views.home, name="home"),
    path("nav", views.nav, name="nav"),
    path("footer", views.footer, name="footer"),
    path("management", views.management, name="management"),

# inventory
    path("create_inventory", views.create_inventory, name="create_inventory"),
    path("edit_inventory/<int:item_id>/", views.edit_inventory, name="edit_inventory"),
    path("list_inventory", views.list_inventory, name="list_inventory"),
    path("detail_inventory/<int:item_id>/", views.inventory_detail, name="inventory_detail"),
    path('delete_inventory/<int:id>/',views.delete_inventory,name='delete_inventory'),


 # order
    path('order/<int:item_id>/', views.create_order, name='create_order'),
    path('item/<int:item_id>/orders_placed/', views.orders_placed, name='orders-placed'),
    path('item/<int:item_id>/orders_received/', views.orders_received, name='orders-received'),
    path('item/<int:item_id>/orders_canceled/', views.orders_canceled, name='orders-canceled'),
    path('item/<int:item_id>/items_sold/', views.items_sold, name='items-sold'),
    path("list_orders", views.list_orders, name="list_orders"),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),

# Transaction
    path('sell/<int:item_id>/', views.sell_item, name='sell_item'),
    path("list_sold", views.list_sold, name="list_sold"),


]
