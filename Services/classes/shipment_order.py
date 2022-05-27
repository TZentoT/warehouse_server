from django.db import models, connection

from .shipment_order_good import ShipmentOrderGood
from ..converters.datetime_converter import DatetimeConverter


class ShipmentOrder(models.Model):

    def get_orders(self, order=0, status='', name="", code=-1):
        data = ""

        try:
            cursor = connection.cursor()
            if order != 0 and status != '' and name == "":
                cursor.execute(f"SELECT * FROM shipment_order WHERE order_id={order} AND status "
                           f"LIKE '{status}' ORDER BY code ASC")
            if order != 0 and status == '' and name == "" and code == -1:
                cursor.execute(f"SELECT * FROM shipment_order WHERE order_id={order} ORDER BY code ASC")
            if order == 0 and status == '' and name == "" and code == -1:
                cursor.execute(f"SELECT * FROM shipment_order ORDER BY code ASC")
            if order == 0 and status != '' and name == "" and code == -1:
                cursor.execute(f"SELECT * FROM shipment_order WHERE status LIKE '{status}%' ORDER BY code ASC")
            if order == 0 and status == '' and name != "" and code == -1:
                cursor.execute(f"SELECT * FROM shipment_order WHERE name LIKE '{name}'")
            if order == 0 and status == '' and name == "" and code != -1:
                cursor.execute(f"SELECT * FROM shipment_order WHERE code={code}")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'shipment_date', 'shipment_status', 'shipment_payment', 'note', 'shipment_price',
                    'requisites', 'status', 'order_id')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f"get_orders {data}")
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def update_orders(self, name="", shipment_date="", shipment_payment="", shipment_price="", code=-1):
        data = ""
        try:
            print(shipment_price)
            cursor = connection.cursor()
            if name != "" and shipment_date != "" and shipment_payment != "" and shipment_price != "" and code != -1:
                cursor.execute(f"UPDATE shipment_order SET name='{name}', shipment_date='{shipment_date}', "
                           f"shipment_payment='{shipment_payment}', shipment_price={shipment_price} "
                               f"WHERE code={code}")
            if name == "" and shipment_date == "" and shipment_payment == "" and shipment_price == "" and code != -1:
                cursor.execute(f"UPDATE shipment_order SET status='closed' WHERE code={code}")
        except Exception as e:
            print(f"update_orders went wrong: {e}")

        return data

    def delete_orders(self, code):
        data = ""
        try:
            goods = ShipmentOrderGood().get_order_goods(code)
            if len(goods) != 0:
                ShipmentOrderGood().delete_ordered_goods(0, code)
            cursor = connection.cursor()
            cursor.execute(f"DELETE from shipment_order WHERE code={code}")
        except Exception as e:
            print(f"delete_orders went wrong: {e}")

        return data

    def insert_orders(self, code, name, shipment_date, shipment_status, shipment_payment, shipment_price, status,
                      order_id):
        data = ""
        try:
            date = DatetimeConverter().convert(shipment_date)
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shipment_order (code, name, shipment_date, shipment_status, shipment_payment, "
                           f"shipment_price, status, order_id) VALUES ({code}, '{name}', '{date}',"
                           f"'{shipment_status}', '{shipment_payment}', '{shipment_price}', '{status}', {order_id})")
        except Exception as e:
            print(f"insert_orders went wrong: {e}")

        return data

