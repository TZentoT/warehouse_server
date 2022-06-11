import json

from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async
from .rack import Rack

from Services.converters import json_converter, string_converter


class Zone(models.Model):

    def get_zone(self, name=""):
        data = []
        try:
            cursor = connection.cursor()
            if name == "":
                cursor.execute('SELECT * FROM zones ORDER BY code ASC')
            if name != "":
                cursor.execute(f"SELECT * FROM zones WHERE name LIKE '{name}'")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'zone_num', 'center_point', 'rotation', 'zone_type_id', 'type')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'Zone get_zone res {result}')
            data = result
        except Exception as e:
            print(f"Zone get_zone went wrong: {e}")

        return data

    def insert(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        print(f"Zone insert {data}")
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO zones (code, name, zone_num, center_point, rotation, "
                           f"zone_type_id, type)"
                           f"VALUES ({data['id']}, '{data['name']}', {data['id']}, '{data['center_point']}', "
                           f"'{data['rotation']}', {data['zone_type_id']}, '{data['type']}')")
            print(f"Zone insert res {data['id']}")

        except Exception as e:
            print(f"Zone insert went wrong: {e}")

        return data

    def update(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        print(f"Zone update {data}")
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE zones SET name='{data['name']}', center_point='{data['center_point']}', "
                           f"rotation='{data['rotation']}', zone_type_id='{data['zone_type_id']}' WHERE code={data['id']}")
            print(f'Zone update res {data}')
        except Exception as e:
            print(f"Zone update went wrong: {e}")

        return data

    def delete(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        print(f"Zone delete {data}")
        try:
            Rack().delete({}, data['id'])
            cursor = connection.cursor()
            cursor.execute(f"DELETE from zones WHERE code={data['id']}")
            print(f'Zone delete res {data}')
        except Exception as e:
            print(f"Zone delete went wrong: {e}")

        return data