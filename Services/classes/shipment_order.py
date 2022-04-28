from django.db import models, connection

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
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def get_orders(self, order):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM shipment_order WHERE order_id={order} AND status ORDER BY code ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'shipment_date', 'shipment_status', 'shipment_payment', 'note', 'shipment_price',
                    'requisites', 'status', 'order_id')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def get_orders(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM shipment_order AND status ORDER BY code ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'shipment_date', 'shipment_status', 'shipment_payment', 'note', 'shipment_price',
                    'requisites', 'status', 'order_id')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def update_orders(self, name, shipment_date, shipment_payment, shipment_price, code):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE shipment_order SET name='{name}', shipment_date='{shipment_date}', "
                           f"shipment_payment='{shipment_payment}', shipment_price='{shipment_price}' WHERE code={code}")
        except Exception as e:
            print(f"update_orders went wrong: {e}")

        return data

    def delete_orders(self, code):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"DELETE from shipment_order WHERE code={code}")
        except Exception as e:
            print(f"delete_orders went wrong: {e}")

        return data

    def insert_orders(self, code, name, shipment_date, shipment_status, shipment_payment, shipment_price, status,
                      order_id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shipment_order (code, name, shipment_date, shipment_status, shipment_payment, "
                           f"shipment_price, status, order_id) VALUES ({code}, {name}, {shipment_date},"
                           f"{shipment_status}, {shipment_payment}, {shipment_price}, {status}, {order_id})")
        except Exception as e:
            print(f"insert_orders went wrong: {e}")

        return data

    def get_orders_with_fullness(self, order, status):
        data = self.get_orders(order, status)
        try:
            for order in data:
                fullness = ShipmentOrderGoods.get_ordered_goods(order["code"])
                if (len(fullness) == 0):
                    fullness = "Пустой"

                else:
                    fullness = "Ожидается"

                order["status_fullness"] = fullness
        except Exception as e:
            print(f"get_orders_with_fullness went wrong: {e}")

        return data
