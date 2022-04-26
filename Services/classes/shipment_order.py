from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async

from .shipment_order_good import ShipmentOrderGoods


class ShipmentOrder(models.Model):

    def get_orders(self, order, status):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM shipment_order WHERE order_id={order} AND status "
                           f"LIKE '{status}' ORDER BY code ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'shipment_date', 'shipment_status', 'shipment_payment', 'note', 'shipment_price',
                    'requisites', 'status', 'order_id')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result

            # TODO разнести методы
            for order in data:
                order["status_fullness"] = ShipmentOrderGoods.get_ordered_goods(order["code"])

        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data
