import base64
import json

from django.db import models, connection

from ..classes.shipment_order import ShipmentOrder
from ..classes.shipment_order_good import ShipmentOrderGood
from ..classes.order import Order
from ..classes.order_good import OrderGoods
from ..classes.shelf import Shelf
from ..classes.rack import Rack
from ..classes.zone import Zone
from ..classes.shelf_space import ShelfSpace
from ..classes.good_type import GoodType
from ..classes.invoice import Invoice
from ..classes.shelf_virtual import ShelfVirtual
from ..classes.rack_virtual import RackVirtual
from ..classes.zone_virtual import ZoneVirtual
from ..classes.goods_type_virtual import GoodsTypeVirtual

from ..converters import json_converter, string_converter


class Orders(models.Model):

    def update_shipment_order_goods(self, body):
        data = ""
        shipment_status = 'Не доставлено'
        shipment_payment = ''
        shipment_orders_in_db = []
        array_for_delete = []

        array_id = ShipmentOrder().get_orders()
        new_id = 1
        if len(array_id) != 0:
            new_id = array_id[len(array_id) - 1]['code']
        iterator = 1

        for shipment in body['tablelist']:
            if shipment['shipmentCost'] == "0":
                shipment_payment = 'Без доставки'
            else:
                shipment_payment = "Не оплачено"

            if shipment['code'] == "":
                ShipmentOrder().insert_orders(new_id + iterator, shipment['shipmentNumber'], shipment['shipmentDate'],
                                              shipment_status, shipment_payment,
                                              int(shipment['shipmentCost'], 'opened'), body['order_id'])

                order_num = new_id + iterator
                if len(shipment['goodsInOrder']) != 0:
                    for good in shipment['goodsInOrder']:
                        array_id = self.get_order_goods()
                        new_id = array_id[len(array_id) - 1]['code']
                        self.insert_ordered_goods(new_id + iterator, good['goodCode'], good['expectingAmount'],
                                                  order_num)
                        iterator += 1
                iterator += 1
            else:
                check = True
                shipmentFromBd = ''
                shipment_orders_in_db = ShipmentOrder().get_orders(body['order_id'])
                for sample in shipment_orders_in_db:
                    if sample['code'] == shipment['code']:
                        check = False
                        shipmentFromBd = sample
                if check:
                    array_for_delete.append(shipmentFromBd)
                else:
                    ShipmentOrder().update_orders(shipment['shipmentNumber'], shipment['shipmentDate'],
                                                  shipment_payment, int(shipment['shipmentCost']), shipment['code'])
                    iterator = 1
                    for good in shipment['goodsInOrder']:
                        if good['shipmentOrderGoodsCode'] == 0:
                            array_id = self.get_order_goods()
                            new_id = array_id[len(array_id) - 1]['code']
                            self.insert_ordered_goods(new_id + iterator, good['goodCode'], good['expectingAmount'],
                                                      good['code'])
                            iterator += 1
                        else:
                            self.update_ordered_goods(good['expectingAmount'], good['shipmentOrderGoodsCode'])

                    shipmentOrderGoodsFromBd = self.get_order_goods(shipment['code'])
                    for good in shipment['goodsInOrder']:
                        check = True
                        for good1 in shipmentOrderGoodsFromBd:
                            if good['goodCode'] == good1['goods']:
                                check = False
                            if check:
                                self.delete_ordered_goods(good['shipmentOrderGoodsCode'], 0)

        return data

    def get_orders_with_fullness(self, order, status):
        data = ShipmentOrder().get_orders(order, status)
        try:
            for order in data:
                fullness = ShipmentOrderGood.get_ordered_goods(order["code"])
                if (len(fullness) == 0):
                    fullness = "Пустой"

                else:
                    fullness = "Ожидается"

                order["status_fullness"] = fullness
        except Exception as e:
            print(f"get_orders_with_fullness went wrong: {e}")

        return data

    def get_shipment_orders(self, order_type, status):
        data = []
        orders = Order().get_orders('', order_type)
        shipments = ShipmentOrder().get_orders(0, status)
        print(orders)
        print(shipments)
        for shipment in shipments:
            for order in orders:
                if order['id'] == shipment['order_id']:
                    data.append(shipment)

        return data

    def post_new_order_with_goods(self, body):
        data = ''
        datatable = body
        datatable = json.loads(datatable)
        datatable = json_converter.JsonConverter().convert(datatable)
        print(f"body: {datatable[0]}")
        if datatable[0]['order_status'] == 'На продажу':
            datatable[0]['order_status'] = 'sell'
        else:
            datatable[0]['order_status'] = 'purchase'

        new_id = 1
        array = Order().get_orders()
        if len(array) != 0:
            new_id = array[-1]['id'] + 1

        Order().insert_order(new_id, datatable[0]['cost'], datatable[0]['deadline'], datatable[0]['order_status'],
                             datatable[0]['address'], datatable[0]['note'], datatable[0]['name'])
        new_good_id = 1
        array = OrderGoods().get_order_goods()
        if len(array) != 0:
            new_good_id = array[-1]['id']

        for good in datatable[0]['order_goods']:
            new_good_id += 1
            print(good)
            OrderGoods().insert_order_good(new_good_id, int(good['goodCode']), new_id, good['amount'],
                                           int(good['cost']))
        return "Новый заказ добавлен"

    def post_goods_to_shelf_space(self, body):
        list_sorted = []
        datatable = body
        datatable = json.loads(datatable)
        datatable = json_converter.JsonConverter().convert(datatable)

        shelfs = Shelf().get_shelfs()
        racks = Rack().get_rack()
        zones = Zone().get_zone()
        print(f"datatable: {datatable}")
        print(f"shelfs: {shelfs}")
        print(f"racks: {racks}")
        print(f"zones: {zones}")

        for element in datatable:
            if element['zone'] != "" and element['rack'] != " " and element['shelf'] != "  ":
                list_sorted.append(element)
                zone_ID = 0
                rack_ID = 0
                shelf_ID = 0

                for zone in zones:
                    if zone['name'] == element['zone']:
                        zone_ID = zone['code']

                for rack in racks:
                    if rack['name'] == element['rack'] and zone_ID == rack['zone_num']:
                        rack_ID = rack['code']

                for shelf in shelfs:
                    if shelf['name'] == element['shelf'] and rack_ID == shelf['rack_num']:
                        shelf_ID = shelf['code']

                ShelfSpace().insert(element['goodCode'], 1, shelf_ID)
                ShipmentOrderGood.update_ordered_goods(-1, -1, element['shipmentOrderGoodsCode'])

        return "post_goods_to_shelf_space complited"

    def update_order_goods_expend(self, code, amount):
        ordered_goods = ShipmentOrderGood().get_order_goods(code)
        ShipmentOrderGood().update_ordered_goods(amount, -1, code)
        GoodType().update(amount, code)
        ShipmentOrder.update_orders("", "", "", "", code)

        return "update_order_goods_expend complited"

    def update_shipment_orders(self, body):
        self.data = []
        datatable = body
        datatable = json.loads(datatable)
        datatable = json_converter.JsonConverter().convert(datatable)

        shipment_orders_opened = ShipmentOrder().get_orders(int(datatable[0]['orderCode']), "opened")
        shipment_orders_closed = ShipmentOrder().get_orders(int(datatable[0]['orderCode']), "closed")
        print(f"shipment_orders {shipment_orders_opened}")
        print(f"shipment_orders_closed {shipment_orders_closed}")
        print(f"data {datatable}")
        shipment_orders = shipment_orders_opened + shipment_orders_closed

        shipment_orders_all = ShipmentOrder().get_orders()
        new_id = 1
        if len(json_converter.JsonConverter().convert(shipment_orders_all)) != 0:
            new_id = json_converter.JsonConverter().convert(shipment_orders_all)[-1]['code'] + 1

        for data in datatable:
            isNew = True
            payment_status = 'Без доставки'
            if data['id'] != -1:
                if int(data['shipmentCost']) != 0:
                    payment_status = 'Не оплачено'
                for shipment_order in shipment_orders:
                    if data['code'] == shipment_order['code']:
                        print(data)
                        isNew = False
                        ShipmentOrder().update_orders(data['shipmentNumber'], data['shipmentDate'], payment_status,
                                                      data['shipmentCost'], data['code'])
                        shipment_orders.remove(shipment_order)
                if isNew and data['shipmentNumber'] != '-':
                    ShipmentOrder().insert_orders(new_id, data['shipmentNumber'], data['shipmentDate'], payment_status,
                                                  'Не доставлено', data['shipmentCost'], 'opened', data['orderCode'])
                    self.data.append(new_id)
                    new_id += 1

        if len(shipment_orders) > 0:
            for shipment_order in shipment_orders:
                if shipment_order['status'] != 'closed':
                    ShipmentOrder().delete_orders(shipment_order['code'])

        return self.data

    def get_shipment_order_goods(self, shipment):
        goods = []
        shipment = ShipmentOrder().get_orders(0, '', "", shipment)
        if shipment != []:
            goods = ShipmentOrderGood().get_order_goods(shipment[0]['code'])
            for good in goods:
                goods_type = GoodType().get_good_types(good['goods'])
                good['goods'] = goods_type[0]['name']
                good['weight'] = goods_type[0]['weight']
                good['order_code'] = goods_type[0]['code']

        return goods

    def post_shipment_goods(self, body):
        self.data = []
        datatable = body
        datatable = json.loads(datatable)
        datatable = json_converter.JsonConverter().convert(datatable)
        shipment = ShipmentOrder().get_orders(0, '', "", datatable[0]['shipmentNumber'])
        goods = ShipmentOrderGood().get_order_goods(shipment[0]['code'])

        goods_all = json_converter.JsonConverter().convert(ShipmentOrderGood().get_order_goods())
        new_id = 1
        if len(goods_all) != 0:
            new_id = int(goods_all[-1]['code'])

        for data in datatable:
            if datatable[0]['id'] != -1:
                isNew = True
                for good in goods:
                    if data['code'] == good['code']:
                        isNew = False
                        ShipmentOrderGood().update_ordered_goods(data['expectingAmount'], -1, data['code'])
                        goods.remove(good)
                if isNew:
                    new_id += 1
                    ShipmentOrderGood().insert_ordered_goods(new_id, data['goodCode'], data['realAmount'],
                                                             shipment[0]['code'], data['realAmount'],
                                                             data['expectingAmount'])
                    self.data.append(new_id)

        for good in goods:
            ShipmentOrderGood().delete_ordered_goods(good['code'])

        return self.data

    def update_deliveries(self, body):
        datatable = body
        datatable = json.loads(datatable)
        datatable = json_converter.JsonConverter().convert(datatable)

        # print(f"datable {datatable}")
        # print(f"datable {datatable[0]['doc']}")

        for data in datatable:
            ShipmentOrderGood().update_ordered_goods(-1, data['amount'], data['code'])

        ShipmentOrder().update_orders("", "", "", "", datatable[0]['orderCode'])

        status = ""
        if datatable[0]['type'] == "Приход":
            status = 'Принято'
        else:
            status = 'Отправлено'
        order_id = ShipmentOrder().get_orders(0, '', "", int(datatable[0]['orderCode']))[0]['order_id']
        # doc = base64.b64 decode(datatable[0]['doc'])
        # print(doc)

        Invoice().insert(int(datatable[0]['account']), order_id, datatable[0]['date'],
                        status, datatable[0]['type'], 1, datatable[0]['orderCode'], datatable[0]['doc'])

        # print(f"update_deliveries {body}")

        return "update_shipment_orders completed"

    def update_shelves_space(self, body):
        self.data = []
        datatable = body
        datatable = json.loads(datatable)
        datatable = json_converter.JsonConverter().convert(datatable)

        zones = Zone().get_zone(datatable[0]['zone'])
        racks = Rack().get_rack(datatable[0]['rack'], zones[0]['code'])
        shelves = Shelf().get_shelfs(datatable[0]['shelf'], racks[0]['code'])

        for data in datatable:
            self.data.append(data['inventaryzationStatus'])
            ShelfSpace().update(shelves[0]['code'], data['shelfSpaceCode'], data['inventaryzationStatus'])

        return self.data

    def get_virtual_rack_with_shelves(self):
        data = {}
        racks = RackVirtual().get()
        shelves = ShelfVirtual().get()

        for rack in racks:
            shelves_dump = {}
            pos = 0
            for shelf in shelves:
                if shelf['rack_id'] == rack['code']:
                    pos += 1
                    shelves_dump[f"shelf_{pos}"] = {}
                    shelves_dump[f"shelf_{pos}"] = shelf
                    # shelves_dump.append(shelf)
            rack['shelves'] = shelves_dump
        data = racks
        print(f"get_virtual_rack_with_shelves res {data}")
        return data

    def get_warehouse_model(self):
        zones = Zone().get_zone()
        iterator = 0
        for zone in zones:
            racks = Rack().get_rack("", zone['code'])
            zone_buf = []
            for rack in racks:
                shelves = Shelf().get_shelfs("", rack['code'])
                shelf_buf = []
                for shelf in shelves:
                    goods_stored = ShelfSpace().get_shelf_space(shelf['code'])
                    good_with_all_info = []
                    for good in goods_stored:
                        good_with_all_info.append(self.get_good_stored_with_all_info(good, iterator))
                        iterator += 1
                    shelf['space'] = good_with_all_info
                    shelf_buf.append(shelf)

                rack['shelfs'] = shelf_buf
                zone_buf.append(rack)
            zone['racks'] = zone_buf

        return zones

    def get_good_stored_with_all_info(self, good, good_id):
        goods_type = GoodType().get_good_types_with_cats()

        for good_type in goods_type:
            if good_type['code'] == good['good']:
                good['id'] = good_id
                good['name'] = good_type['name']
                good['category'] = good_type['subcategory_2']
                good['subCategory'] = good_type['subcategory_3']
                good['cost'] = good_type['price']
                good['goodTypeId'] = good_type['virtual_type']
                good['weight'] = good_type['weight']
                good['goodCharacteristics'] = good_type['description']


        return json_converter.JsonConverter().convert(good)

    def get_goods_type_with_virtual_params(self):
        data = []
        goods_type_virtual = GoodsTypeVirtual().get()

        for good_type_virtual in goods_type_virtual:
            body = {
                'virtual_id': good_type_virtual['id'],
                'text': good_type_virtual['name'],
                'depth': good_type_virtual['depth'],
                'width': good_type_virtual['width'],
                'height': good_type_virtual['height'],
                'color': good_type_virtual['color'],
                'translation': good_type_virtual['translation']
            }
            data.append(body)

        return data

    def get_zones_racks_shelves(self):
        data = []
        zones = Zone().get_zone()
        for zone in zones:
            racks = Rack().get_rack("", zone['code'])
            for rack in racks:
                shelves = Shelf().get_shelfs("", rack['code'])
                shelves.insert(0, {'menuItem': ""})
                rack['shelves'] = shelves
            racks.insert(0, {'menuItem': ""})
            zone['racks'] = racks
        data = zones

        return data
