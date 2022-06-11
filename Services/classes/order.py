import json

from django.db import models, connection
import datetime

from Services.converters import json_converter


class Order(models.Model):

    def get_orders(self, status_execution='', order_status=''):
        data = []
        try:
            cursor = connection.cursor()
            if status_execution != '' and order_status == '':
                cursor.execute(f"SELECT * FROM orders WHERE status_execution LIKE '{status_execution}' ORDER BY id ASC")
            if status_execution == '' and order_status != '':
                cursor.execute(f"SELECT id FROM orders WHERE order_status LIKE '{order_status}' ORDER BY id ASC")
            if order_status == '' and status_execution == '':
                cursor.execute(f"SELECT * FROM orders ORDER BY id ASC")
            if status_execution != '' and order_status != '':
                cursor.execute(f"SELECT * FROM orders WHERE order_status LIKE '{order_status}' "
                               f"AND status_execution LIKE '{status_execution}' ORDER BY id ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('id', 'operator', 'cost', 'deadline', 'status_execution', 'document', 'requisites',
                    'payment_status', 'order_status', 'address', 'note', 'name')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'get_orders res {data}')
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def update_orders(self, body):
        data = json.loads(body)
        data = json_converter.JsonConverter().convert(data)
        id = json_converter.JsonConverter().convert(data)['id']
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE orders SET status_execution = '{'complited'}' WHERE id={id}")
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def insert_order(self, id, cost, deadline, order_status, address, note, name):
        data = ""
        try:
            deadline = str(deadline).split('-')
            deadline = datetime.date(int(deadline[0]), int(deadline[1]), int(deadline[2]))
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO orders (id, cost, deadline, order_status, address, note, name) "
                           f"VALUES ({id}, {cost}, '{deadline}', '{order_status}', '{address}', '{note}', '{name}')")
        except Exception as e:
            print(f"insert_order went wrong: {e}")

        return data


