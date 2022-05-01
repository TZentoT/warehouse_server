from django.shortcuts import render
from django.http import HttpResponse
from .classes import zone, color, rack, client, order, good_type, shipment_order, shipment_order_good, order_good
from .converters import string_converter

from asgiref.sync import sync_to_async


# Create your views here.

def colors(request, *args):
    result = color.Color().get_color()
    return HttpResponse(string_converter.StringConverter().convert(result))


def zones(request, *args):
    result = zone.Zone().get_zone()
    return HttpResponse(string_converter.StringConverter().convert(result))


def racks(request, path):
    result = ""
    if path == '/racks':
        result = rack.Rack().getRack()

    if path == '/racks_by_zone':
        result = rack.Rack().getRack(1)

    return HttpResponse(string_converter.StringConverter().convert(result))


def shelfs(request, path):
    result = ""
    if path == "/shelfs":
        result = "getShelfs"

    if path == "/shelfs_by_racks":
        result = "getShipmentOrderGoods"

    return HttpResponse(string_converter.StringConverter().convert(result))


def shipment_orders(request, path):
    result = ""
    if path == "/shipment_order_goods":
        order_type = request.GET.get('type')
        status = request.GET.get('status')
        result = shipment_order.ShipmentOrder().get_shipment_orders(order_type, status)

    if path == "/shipment_order_goods_id":
        status = request.GET.get('status')
        order_id = request.GET.get('order_id')
        result = shipment_order.ShipmentOrder().get_orders_with_fullness(order_id, status)

    if path == "/shipment_order_goods_all":
        result = "getShipmentOrderGoodsAll"

    if path == "/update_shipment_orders":
        # TODO написать код
        result = "updateShipmentOrders"

    return HttpResponse(string_converter.StringConverter().convert(result))


def orders(request, path):
    result = ""

    if path == "/orders":
        # TODO написать код
        result = "getOrders"

    if path == "/orders_all":
        status = request.GET.get('status')
        print(status)
        result = order.Order().get_orders(status)

    if path == "/orders_goods":
        order_id = request.GET.get('order_id')
        result = order_good.OrderGoods().get_good_types_by_order(order_id)

    if path == "/shipment_order_goods_by_order":
        code = request.GET.get("code")
        result = shipment_order_good.ShipmentOrderGoods().get_ordered_goods(code)

    if path == "/update_order":
        result = "updateOrder"

    if path == "/update_order_goods":
        result = "updateOrderGoods"

    if path == "/update_order_goods_expend":
        result = "updateOrderGoodsExpend"

    if path == "/update_order_status":
        id = request.GET.get("id")
        result = order.Order().update_orders(id)

    if path == "/post_order":
        result = "postNewOrder"

    return HttpResponse(string_converter.StringConverter().convert(result))


def clients(request, path):
    result = ""

    if path == "/clients":
        result = client.Client().get_client()

    if path == "/post_user":
        body = request.body.decode('UTF-8')
        result = client.Client().update_client_datatable(body)

    return HttpResponse(string_converter.StringConverter().convert(result))


def types(request, path):
    result = ""

    if path == "/goods_type_code":
        result = "getGoodsTypeByCode"

    if path == "/goods_type_cats":
        result = good_type.GoodType().get_good_types_with_cats()

    if path == "/goods_type":
        result = good_type.GoodType().get_good_types()

    if path == "/update_inventory":
        result = "updateInventory"

    return HttpResponse(string_converter.StringConverter().convert(result))


def categories(request, path):
    result = ""

    if path == "/goods_cat":
        result = "getCategories"

    if path == "/goods_subcat2":
        result = "getSubCategories2"

    if path == "/goods_subcat3":
        result = "getSubCategories3"

    if path == "/goods_subcat4":
        result = "getSubCategories4"

    return HttpResponse(string_converter.StringConverter().convert(result))


def shelf_space(request, path):
    result = ""

    if path == "shelf_space":
        result = "getShelfSpace"

    if path == "shelf_set":
        result = "setShelfs"

    if path == "post_goods_to_shelfs":
        result = "postGoodsToShelfSpace"

    if path == "update_shelf_space_status":
        result = "updateShelfSpaceStatus"

    return HttpResponse(string_converter.StringConverter().convert(result))



