from django.urls import path
from . import views

urlpatterns = [
    path('colors/', views.colors),

    path('zones/', views.zones),

    path('racks/',          views.racks, {'path': '/racks'}),
    path('racks_by_zone/',  views.racks, {'path': '/racks_by_zone'}),

    path('shelfs/', views.shelfs, {'path': '/shelfs'}),
    path('shelfs_by_racks/', views.shelfs, {'path': '/shelfs_by_racks'}),

    path('goods_type_code/',    views.types, {'path': '/goods_type_code'}),
    path('goods_type_cats/',    views.types, {'path': '/goods_type_cats'}),
    path('goods_type/',         views.types, {'path': '/goods_type'}),
    path('update_inventory/',   views.types, {'path': '/update_inventory'}),

    path('goods_cat/',      views.categories, {'path': '/goods_cat'}),
    path('goods_subcat2/',  views.categories, {'path': '/goods_subcat2'}),
    path('goods_subcat3/',  views.categories, {'path': '/goods_subcat3'}),
    path('goods_subcat4/',  views.categories, {'path': '/goods_subcat4'}),

    path('clients/',    views.clients, {'path': '/clients'}),
    path('post_user/',  views.clients, {'path': '/post_user'}),

    path('orders/',                         views.orders, {'path': '/orders'}),
    path('shipment_order_goods_by_order/',  views.orders, {'path': '/shipment_order_goods_by_order'}),
    path('orders_all/',                     views.orders, {'path': '/orders_all'}),
    path('orders_goods/',                   views.orders, {'path': '/orders_goods'}),
    path('post_order/',                     views.orders, {'path': '/post_order'}),
    path('update_order/',                   views.orders, {'path': '/update_order'}),
    path('update_order_goods/',             views.orders, {'path': '/update_order_goods'}),
    path('update_order_goods_expend/',      views.orders, {'path': '/update_order_goods_expend'}),
    path('update_order_status/',            views.orders, {'path': '/update_order_status'}),

    path('update_shelf_space_status/',  views.shelf_spaces, {'path': '/update_shelf_space_status'}),
    path('post_goods_to_shelfs/',       views.shelf_spaces, {'path': '/post_goods_to_shelfs'}),
    path('shelf_space/',                views.shelf_spaces, {'path': '/shelf_space'}),
    path('shelf_set/',                  views.shelf_spaces, {'path': '/shelf_set'}),

    path('update_shipment_orders/',             views.shipment_orders, {'path': '/update_shipment_orders'}),
    path('insert_shipment_orders_by_order/',    views.shipment_orders, {'path': '/insert_shipment_orders_by_order'}),
    path('shipment_order_goods/',               views.shipment_orders, {'path': '/shipment_order_goods'}),
    path('shipment_order_goods_id/',            views.shipment_orders, {'path': '/shipment_order_goods_id'}),
    path('shipment_order_goods_id_all/',            views.shipment_orders, {'path': '/shipment_order_goods_id_all'}),
    path('shipment_order_goods_all/',           views.shipment_orders, {'path': '/shipment_order_goods_all'}),
]
