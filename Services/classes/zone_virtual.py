import json

from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async
from ..converters import string_converter, json_converter
from .zone import Zone
from .rack import Rack

class ZoneVirtual(models.Model):

    def get(self):
        data = []
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM zones_virtual ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'width', 'height', 'color', 'line_width', 'chamfer_length', 'name', 'text_size',
                    'message_alighment')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f"ZoneVirtual get res {result}")
            data = result
        except Exception as e:
            print(f"ZoneVirtual get went wrong: {e}")

        return data

    def insert(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO zones_virtual (code, width, height, color, line_width, "
                           f"chamfer_length, name, text_size, message_alighment)"
                           f"VALUES ({data['id']}, {data['width']}, {data['height']}, '{data['color']}', "
                           f"{data['line_width']}, {data['chamfer_length']}, '{data['name']}', {data['text_size']},"
                           f"'{data['message_alighment']}')")
            print(f"ZoneVirtual insert res {data}")
        except Exception as e:
            print(f"ZoneVirtual insert went wrong: {e}")

        return data

    def update(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE zones_virtual SET width={data['width']}, height={data['height']}, "
                           f"color='{data['color']}', line_width={data['line_width']}, "
                           f"chamfer_length={data['chamfer_length']}, name='{data['name']}', "
                           f"text_size='{data['text_size']}', message_alighment='{data['message_alighment']}' "
                           f"WHERE code={data['id']}")
            print(f"ZoneVirtual update res {data}")
        except Exception as e:
            print(f"ZoneVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = id
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            zones = Zone().get_zone("", data['id'])
            is_possible_to_delete = True
            if len(zones) != 0:
                is_possible_to_delete = False

            if is_possible_to_delete:
                cursor = connection.cursor()
                cursor.execute(f"DELETE from zones_virtual WHERE code={data['id']}")
                print(f"ZoneVirtual delete res {data}")
                data = "Тип зоны успеношно удален"
            else:
                data = "Невозможно удалить. Некоторые зоны привязаны к данному типу зон"
        except Exception as e:
            print(f"ZoneVirtual delete went wrong: {e}")

        return data