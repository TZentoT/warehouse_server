from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async


class Rack(models.Model):

    def get_rack(self, name="", zone_num=0):
        data = ""
        try:
            cursor = connection.cursor()
            if name == "" and zone_num == 0:
                cursor.execute('SELECT * FROM racks ORDER BY code ASC')
            if name != "" and zone_num != 0:
                cursor.execute(f"SELECT * FROM racks WHERE name LIKE '{name}' and zone_num={zone_num} ")
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
