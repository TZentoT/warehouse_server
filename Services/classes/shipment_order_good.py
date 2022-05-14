from django.db import models, connection


class ShipmentOrderGood(models.Model):

    def get_order_goods(self, code=-1):
        data = ""
        try:
            cursor = connection.cursor()
            if code == -1:
                cursor.execute(f"SELECT * FROM shipment_order_goods ORDER BY code ASC")
            if code != -1:
                cursor.execute(f"SELECT * FROM shipment_order_goods WHERE order_num={code}")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'goods', 'amount', 'order_num', 'amount_real', 'placed_amount')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f"get_order_goods res: {result}")
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

    def update_ordered_goods(self, amount=-1, amount_real=-1, code=-1):
        data = ""
        try:
            cursor = connection.cursor()
            if amount != -1 and code != -1:
                cursor.execute(f"UPDATE shipment_order_goods SET amount={amount} WHERE code={code}")
            if amount == -1 and code != -1 and amount_real == -1:
                cursor.execute(f"UPDATE shipment_order_goods SET placed_amount = placed_amount + 1 WHERE code={code}")
            if amount_real != -1 and code != -1 and amount == -1:
                cursor.execute(f"UPDATE shipment_order_goods SET amount_real={amount_real} WHERE code={code}")

            print(f'update_ordered_goods res {data}')
        except Exception as e:
            print(f"update_ordered_goods went wrong: {e}")

        return data

    def insert_ordered_goods(self, code, goods, amount, order_num, amount_real, placed_amount):
        data = ""
        print(f"new_id {code}")
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shipment_order_goods (code, goods, amount, order_num, "
                           f"amount_real, placed_amount) "
                           f"VALUES ({code}, {goods}, {amount}, {order_num}, {amount_real}, {placed_amount})")

            print(f'res {data}')
        except Exception as e:
            print(f"insert_ordered_goods went wrong: {e}")

        return data
