from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async
from ..converters import string_converter


class ZoneVirtual(models.Model):

    def get(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM zones_virtual ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'width', 'height', 'color', 'line_width', 'chamfer_length', 'name', 'text_size',
                    'message_alighment')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'ZoneVirtual get res {result}')
            data = result
        except Exception as e:
            print(f"ZoneVirtual get went wrong: {e}")

        return data

    def insert(self, body):
        data = ""
        try:
            new_id = self.get()[-1]['code'] + 1
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO zones_virtual (code, width, height, color, line_width, "
                           f"chamfer_length, name, text_size, message_alighment)"
                           f"VALUES ({new_id}, {body['width']}, {body['height']}, {body['color']}, "
                           f"{body['line_width']}, {body['chamfer_length']}, {body['name']}, {body['text_size']},"
                           f"{body['message_alighment']})")
            print(f'ZoneVirtual insert res {new_id}')
            data = new_id
        except Exception as e:
            print(f"ZoneVirtual insert went wrong: {e}")

        return data

    def update(self, id, body):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE zones_virtual SET width={body['width']}, height={body['height']}, "
                           f"color={body['color']}, line_width={body['line_width']}, "
                           f"chamfer_length={body['chamfer_length']}, name={body['name']}, "
                           f"text_size='{body['text_size']}', message_alighment={body['message_alighment']} "
                           f"WHERE code={id}")
            print(f'ZoneVirtual update res {data}')
        except Exception as e:
            print(f"ZoneVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE from zones_virtual WHERE code={id}')
            print(f'ZoneVirtual delete res {data}')
            data = data
        except Exception as e:
            print(f"ZoneVirtual delete went wrong: {e}")

        return data