from django.db import models, connection

from Services.converters import datetime_converter


class Invoice(models.Model):

    def get(self, status=""):
        data = ""
        try:
            cursor = connection.cursor()
            if status == "":
                cursor.execute(f"SELECT * FROM invoices ORDER BY code ASC")
            if status != "":
                cursor.execute(f"SELECT * FROM invoices WHERE status LIKE '{status}'")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'operator', 'order_id', 'datetime', 'status', 'invoice_type', 'provider', 'shipment', 'document')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'Invoice get res {result}')
            data = result

        except Exception as e:
            print(f"Invoice get went wrong: {e}")

        return data

    def insert(self, operator, order, date, status, invoice_type, provider, shipment, document):
        try:
            if len(self.get()) == 0:
                new_id = 1
            else:
                new_id = self.get()[-1]['code'] + 1
            date = datetime_converter.DatetimeConverter().convert(date)
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO invoices (code, operator, order_id, datetime, document, status, invoice_type, provider, "
                f"shipment) VALUES ({new_id}, {operator}, {order}, '{date}','{document}', '{status}', "
                f"'{invoice_type}', {provider}, {shipment})")

        except Exception as e:
            print(f"Invoice insert went wrong: {e}")

        return "Invoice insert completed"

    def update(self, code, status):
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE invoices SET status LIKE '{status}' WHERE code={code}")

        except Exception as e:
            print(f"Invoice update wrong: {e}")

        return "Invoice update completed"

    def delete(self, code):
        try:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM invoices WHERE code={code}")

        except Exception as e:
            print(f"Invoice delete wrong: {e}")

        return "Invoice delete completed"
