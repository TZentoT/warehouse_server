from django.db import models, connection

from .shipment_order import ShipmentOrder


class ShipmentOrderGoods(models.Model):

    def get_order_goods(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM shipment_order_goods ORDER BY code ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'goods', 'amount', 'order_num', 'amount_real', 'placed_amount')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def get_ordered_goods(self, code):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM shipment_order_goods WHERE order_num={code} ORDER BY code ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'goods', 'amount', 'order_num', 'amount_real', 'placed_amount')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'res {data}')
        except Exception as e:
            print(f"get_ordered_goods went wrong: {e}")

        return data

    def delete_ordered_goods(self, code=0, order_num=0):
        data = ""
        try:
            cursor = connection.cursor()
            if code != 0:
                cursor.execute(f"DELETE from shipment_order_goods WHERE code={code}")
            elif order_num != 0:
                cursor.execute(f"DELETE from shipment_order_goods WHERE order_num={order_num}")
        except Exception as e:
            print(f"delete_ordered_goods went wrong: {e}")

        return data

    def update_ordered_goods(self, amount, code):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE shipment_order_goods SET amount={amount} WHERE code={code}")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'goods', 'amount', 'order_num', 'amount_real', 'placed_amount')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'res {data}')
        except Exception as e:
            print(f"update_ordered_goods went wrong: {e}")

        return data

    def insert_ordered_goods(self, code, goods, amount, order_num):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shipment_order_goods (code, goods, amount, order_num) "
                           f"VALUES ({code}, {goods}, {amount}, {order_num})")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'goods', 'amount', 'order_num', 'amount_real', 'placed_amount')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'res {data}')
        except Exception as e:
            print(f"update_ordered_goods went wrong: {e}")

        return data

    def update_shipment_order_goods(self, body):
        data = ""
        shipment_status = 'Не доставлено'
        shipment_payment = ''
        shipment_orders_in_db = []
        array_for_delete = []

        array_id = ShipmentOrder().get_orders()
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
                    if sample['code']==shipment['code']:
                        check = False
                        shipmentFromBd = sample
                if check: array_for_delete.append(shipmentFromBd)
                else:
                    ShipmentOrder().update_orders(shipment['shipmentNumber'], shipment['shipmentDate'],
                                                      shipment_payment, int(shipment['shipmentCost']), shipment['code'])
                    iterator = 1
                    for good in shipment['goodsInOrder']:
                        if good['shipmentOrderGoodsCode'] == 0:
                            array_id = self.get_order_goods()
                            new_id = array_id[len(array_id) - 1]['code']
                            self.insert_ordered_goods(new_id+iterator, good['goodCode'], good['expectingAmount'],
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
