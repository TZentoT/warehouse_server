from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async


class Rack(models.Model):

    def get_rack(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM racks ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'rack_num', 'zone_num')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result
        except Exception as e:
            print(f"Smth wrong: {e}")

        return data
