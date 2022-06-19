from django.http import HttpResponse
from .classes import zone, color, rack, client, order, good_type, shipment_order, \
    shipment_order_good, order_good, categories, subcategories_2, subcategories_3, subcategories_4, shelf, \
    shelf_space, rack_virtual, zone_virtual, shelf_virtual, goods_type_virtual
from .sub_classes import orders_requests
from .converters import string_converter, json_converter

from urllib.parse import unquote

# Create your views here.

def colors(request, *args):
    result = json_converter.JsonConverter().convert(color.Color().get_color())
    return HttpResponse(string_converter.StringConverter().convert(result))


def zones(request, path):
    result = ""

    if path == '/zones':
        result = json_converter.JsonConverter().convert(zone.Zone().get_zone())

    if path == '/zones_post':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(zone.Zone().insert(body))

    if path == '/zones_update':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(zone.Zone().update(body))

    if path == '/zones_delete':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(zone.Zone().delete(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def zones_virtual(request, path):
    result = ""
    if path == '/zones_virtual':
        result = zone_virtual.ZoneVirtual().get()

    if path == '/zones_virtual_post':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(zone_virtual.ZoneVirtual().insert(body))

    if path == '/zones_virtual_update':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(zone_virtual.ZoneVirtual().update(body))

    if path == '/zones_virtual_delete':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(zone_virtual.ZoneVirtual().delete(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def racks(request, path):
    result = ""
    if path == '/racks':
        result = json_converter.JsonConverter().convert(rack.Rack().get_rack())

    if path == '/racks_by_zone':
        result = json_converter.JsonConverter().convert(rack.Rack().get_rack(1))

    if path == '/racks_post':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(rack.Rack().insert(body))

    if path == '/racks_update':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(rack.Rack().update(body))

    if path == '/racks_delete':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(rack.Rack().delete(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def racks_virtual(request, path):
    result = ""
    if path == '/racks_virtual':
        result = json_converter.JsonConverter().convert(rack_virtual.RackVirtual().get())

    if path == '/racks_virtual_shelves':
        result = orders_requests.Orders().get_virtual_rack_with_shelves()
        print(f"res: {result}")

    if path == '/racks_virtual_post':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(rack_virtual.RackVirtual().insert(body))

    if path == '/racks_virtual_update':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(rack_virtual.RackVirtual().update(body))

    if path == '/racks_virtual_delete':
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(rack_virtual.RackVirtual().delete(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def shelfs(request, path):
    result = ""
    if path == "/shelfs":
        result = json_converter.JsonConverter().convert(shelf.Shelf().get_shelfs())

    if path == "/shelfs_by_racks":
        result = "getShipmentOrderGoods"

    return HttpResponse(string_converter.StringConverter().convert(result))


def shelfs_virtual(request, path):
    result = ""
    if path == "/shelfs_virtual":
        result = json_converter.JsonConverter().convert(
            json_converter.JsonConverter().convert(shelf_virtual.ShelfVirtual.get()))

    if path == "/shelfs_virtual_insert":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(
            json_converter.JsonConverter().convert(shelf_virtual.ShelfVirtual.insert(body)))

    if path == "/shelfs_virtual_update":
        body = request.body.decode('UTF-8')
        id = body['code']
        result = json_converter.JsonConverter().convert(
            json_converter.JsonConverter().convert(shelf_virtual.ShelfVirtual.update(id, body)))

    if path == "/shelfs_virtual_delete":
        id = body['id']
        result = json_converter.JsonConverter().convert(
            json_converter.JsonConverter().convert(shelf_virtual.ShelfVirtual.delete(id)))

    return HttpResponse(string_converter.StringConverter().convert(result))


def shipment_orders(request, path):
    result = ""
    if path == "/shipment_order_goods":
        order_type = request.GET.get('type')
        status = request.GET.get('status')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().get_shipment_orders(order_type, status))

    if path == "/shipment_order_goods_id":
        status = request.GET.get('status')
        order_id = request.GET.get('order_id')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().get_orders_with_fullness(order_id, status))

    if path == "/shipment_goods_id":
        shipment_num = request.GET.get('shipment_num')
        shipment_num = unquote(shipment_num)
        result = json_converter.JsonConverter().convert(orders_requests.Orders().get_shipment_order_goods(shipment_num))

    if path == "/shipment_order_goods_all":
        result = json_converter.JsonConverter().convert(shipment_order_good.ShipmentOrderGood().get_order_goods())

    if path == "/shipment_order_goods_id_all":
        order_id = request.GET.get('order_id')
        result = json_converter.JsonConverter().convert(shipment_order.ShipmentOrder().get_orders(order_id))

    if path == "/update_shipment_orders":
        # TODO написать код
        result = "updateShipmentOrders"

    if path == "/insert_shipment_orders_by_order":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().update_shipment_orders(body))

    if path == "/insert_shipment_goods":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().post_shipment_goods(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def orders(request, path):
    result = ""

    if path == "/orders":
        order_status = request.GET.get('type')
        status_execution = request.GET.get('status')
        result = json_converter.JsonConverter().convert(order.Order().get_orders(status_execution, order_status))

    if path == "/orders_all":
        status = request.GET.get('status')
        result = json_converter.JsonConverter().convert(order.Order().get_orders(status))

    if path == "/orders_goods":
        order_id = request.GET.get('order_id')
        result = json_converter.JsonConverter().convert(order_good.OrderGoods().get_good_types_by_order(order_id))

    if path == "/shipment_order_goods_by_order":
        code = request.GET.get("code")
        result = json_converter.JsonConverter().convert(shipment_order_good.ShipmentOrderGood().get_ordered_goods(code))

    if path == "/update_order":
        result = "updateOrder"

    if path == "/update_order_goods":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().update_deliveries(body))

    if path == "/update_order_goods_expend":
        amount = request.GET.get('amount')
        code = request.GET.get('code')
        result = json_converter.JsonConverter().convert(orders_requests.update_order_goods_expend(code, amount))

    if path == "/update_order_status":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(order.Order().update_orders(body))

    if path == "/post_order":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().post_new_order_with_goods(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def clients(request, path):
    result = ""

    if path == "/clients":
        result = json_converter.JsonConverter().convert(client.Client().get_client())

    if path == "/client_avatar":
        id = request.GET.get('id')
        result = json_converter.JsonConverter().convert(client.Client().get_img_avatar(id))

    if path == "/post_user":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(client.Client().update_client_datatable(body))

    if path == "/update_user":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(client.Client().update_existing_client(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def types(request, path):
    result = ""

    if path == "/goods_type_code":
        result = "getGoodsTypeByCode"

    if path == "/goods_type_cats":
        result = json_converter.JsonConverter().convert(good_type.GoodType().get_good_types_with_cats())

    if path == "/goods_type":
        result = json_converter.JsonConverter().convert(good_type.GoodType().get_good_types())

    if path == "/goods_type_post":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(good_type.GoodType().insert(body))

    if path == "/update_inventory":
        result = "updateInventory"

    return HttpResponse(string_converter.StringConverter().convert(result))


def types_virtual(request, path):
    result = ""

    if path == "/goods_type_virtual":
        result = goods_type_virtual.GoodsTypeVirtual().get()

    if path == "/goods_type_with_virtual_info":
        result = orders_requests.Orders().get_goods_type_with_virtual_params()

    if path == "/goods_type_insert":
        body = request.body.decode('UTF-8')
        result = goods_type_virtual.GoodsTypeVirtual().insert(body)

    if path == "/goods_type_update":
        body = request.body.decode('UTF-8')
        result = goods_type_virtual.GoodsTypeVirtual().update(body)

    if path == "/goods_type_delete":
        body = request.body.decode('UTF-8')
        result = goods_type_virtual.GoodsTypeVirtual().delete(body)

    return HttpResponse(string_converter.StringConverter().convert(result))


def categories(request, path):
    result = ""

    if path == "/goods_cat":
        result = json_converter.JsonConverter().convert(categories.Categories().get_categories())

    if path == "/goods_subcat2":
        result = json_converter.JsonConverter().convert(subcategories_2.Subcategories2().get_subcategories())

    if path == "/goods_subcat3":
        result = json_converter.JsonConverter().convert(subcategories_3.Subcategories3().get_subcategories())

    if path == "/goods_subcat4":
        result = json_converter.JsonConverter().convert(subcategories_4.Subcategories4().get_categories())

    return HttpResponse(string_converter.StringConverter().convert(result))


def shelf_spaces(request, path):
    result = ""

    if path == "/shelf_space":
        result = json_converter.JsonConverter().convert(shelf_space.ShelfSpace().get_shelf_space())

    if path == "/shelf_set":
        result = "setShelfs"

    if path == "/post_goods_to_shelfs":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().post_goods_to_shelf_space(body) )

    if path == "/update_shelf_space_status":
        body = request.body.decode('UTF-8')
        result = json_converter.JsonConverter().convert(orders_requests.Orders().update_shelves_space(body))

    return HttpResponse(string_converter.StringConverter().convert(result))


def warehouse(request, path):
    result = ""

    if path == "/warehouse_model":
        result = orders_requests.Orders().get_warehouse_model()

    if path == "/warehouse_all_types":
        result = orders_requests.Orders().get_zones_racks_shelves()

    return HttpResponse(string_converter.StringConverter().convert(result))

