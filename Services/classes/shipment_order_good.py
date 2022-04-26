from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async


class ShipmentOrderGoods(models.Model):

    def get_ordered_goods(self, code):
        data = ""
        fullness = "Пустой"
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

            # TODO разнести методы
            if (len(data) == 0):
                fullness = "Пустой"

            else:
                fullness = "Ожидается"

        except Exception as e:
            print(f"get_ordered_goods went wrong: {e}")

        return fullness


