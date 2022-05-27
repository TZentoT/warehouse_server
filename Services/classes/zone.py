from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async


class Zone(models.Model):

    def get_zone(self, name=""):
        data = ""
        try:
            cursor = connection.cursor()
            if name == "":
                cursor.execute('SELECT * FROM zones ORDER BY code ASC')
            if name != "":
                cursor.execute(f"SELECT * FROM zones WHERE name LIKE '{name}'")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'zone_num', 'width', 'length', 'color', 'line_width', 'chamfer_length', 'text_size',
                    'message_alighment')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result
        except Exception as e:
            print(f"Smth wrong: {e}")

        return data
