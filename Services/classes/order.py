from django.db import models, connection


class Order(models.Model):

    def get_orders(self, status):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM orders WHERE status_execution LIKE '{status}' ORDER BY id ASC")
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


