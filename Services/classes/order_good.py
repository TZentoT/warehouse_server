from ..converters import json_converter
from django.db import models, connection

from .good_type import GoodType


class OrderGoods(models.Model):

    def get_order_goods(self, order_id=0):
        data = []
        try:
            cursor = connection.cursor()
            if order_id != 0:
                cursor.execute(f"SELECT * FROM order_goods WHERE order_id={order_id} ORDER BY id ASC")
            if order_id == 0:
                cursor.execute(f"SELECT * FROM order_goods ORDER BY id ASC")
            rows = cursor.fetchall()
            result = []
            keys = ("id", "good_id", "order_id", "amount", "price_one")
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'get_order_goods res {data}')
        except Exception as e:
            print(f"get_order_goods went wrong: {e}")

        return data

    def get_good_types_by_order(self, order_id):
        goods = []
        try:
            data = self.get_order_goods(order_id)
            data = json_converter.JsonConverter().convert(data)
            good_types = GoodType().get_good_types()
            good_types = json_converter.JsonConverter().convert(good_types)

            for order in data:
                for good in good_types:
                    if good["code"] == order["good_id"]:
                        good["amount"] = order["amount"]
                        good["price"] = order["price_one"]
                        goods.append(good)

            print(f"get_good_types_by_order res {goods}")
        except Exception as e:
            print(f"get_good_types_by_order went wrong: {e}")

        return goods

    def insert_order_good(self, new_id, good_id, order_id, amount, price_one):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO order_goods (id, good_id, order_id, amount, price_one) "
                           f"VALUES ({new_id}, {good_id}, {order_id}, {amount}, {price_one})")
        except Exception as e:
            print(f"insert_order_good went wrong: {e}")

        return data