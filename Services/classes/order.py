from django.db import models, connection


class Order(models.Model):

    def get_orders(self, status_execution='', order_status=''):
        data = ""
        try:
            cursor = connection.cursor()
            if status_execution!='':
                cursor.execute(f"SELECT * FROM orders WHERE status_execution LIKE '{status_execution}' ORDER BY id ASC")
            if order_status!='':
                cursor.execute(f"SELECT id FROM orders WHERE order_status LIKE '{order_status}' ORDER BY id ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('id', 'operator', 'cost', 'deadline', 'status_execution', 'document', 'requisites',
                    'payment_status', 'address', 'note', 'name')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'res {data}')
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data

    def update_orders(self, id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE orders SET status_execution = '{'complited'}' WHERE id={id}")
        except Exception as e:
            print(f"getOrders went wrong: {e}")

        return data


