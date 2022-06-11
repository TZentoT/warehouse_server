import json

from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async

from Services.converters import json_converter
from .shelf import Shelf

class Rack(models.Model):

    def get_rack(self, name="", zone_num=0):
        data = []
        try:
            cursor = connection.cursor()
            if name == "" and zone_num == 0:
                cursor.execute('SELECT * FROM racks ORDER BY code ASC')
            if name != "" and zone_num != 0:
                cursor.execute(f"SELECT * FROM racks WHERE name LIKE '{name}' and zone_num={zone_num} ")
            if name == "" and zone_num != 0:
                cursor.execute(f"SELECT * FROM racks WHERE zone_num={zone_num} ")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'rack_num', 'zone_num', 'center_point', 'rotation', 'rack_type_id', 'type')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'Rack get_rack res {result}')
            data = result
        except Exception as e:
            print(f"Rack get_rack went wrong: {e}")

        return data

    def insert(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        print(f"Rack insert {data}")
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO racks (code, name, rack_num, zone_num, center_point, rotation, "
                           f"rack_type_id, type)"
                           f"VALUES ({data['id']}, '{data['name']}', {data['id']}, '{data['zone_num']}', "
                           f"'{data['center_point']}', {data['rotation']}, '{data['rack_type_id']}', "
                           f"'{data['type']}')")

            print(f"Rack insert res {data['id']}")

        except Exception as e:
            print(f"Rack insert went wrong: {e}")

        return data

    def update(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        print(f"Rack update {data}")
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE racks SET name='{data['name']}', center_point='{data['center_point']}', "
                           f"rotation='{data['rotation']}', zone_type_id='{data['zone_type_id']}' WHERE zone_num={data['id']}")
            print(f'Rack update res {data}')
        except Exception as e:
            print(f"Rack update went wrong: {e}")

        return data

    def delete(self, body={}, id=-1):
        data = {}
        if body != {}:
            data = body
            data = json.loads(data)
            data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            if id == -1:
                racks = self.get_rack("", data['id'])
                for rack in racks:
                    Shelf().delete({}, rack['code'])
                cursor.execute(f"DELETE from racks WHERE zone_num={data['id']}")
            if id != -1:
                racks = self.get_rack("", id)
                for rack in racks:
                    Shelf().delete({}, rack['code'])
                cursor.execute(f"DELETE from racks WHERE zone_num={id}")
            print(f'Rack delete res {data}')
            data = data
        except Exception as e:
            print(f"Rack delete went wrong: {e}")

        return data