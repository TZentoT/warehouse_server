from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async


class RackVirtual(models.Model):

    def get(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM racks_virtual ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'depth', 'shelf_width', 'shelf_height', 'columns_amount',
                    "rows_amount", 'border_width', 'free_space_x', 'free_space_y', 'color', 'translation')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'RackVirtual get res {result}')
            data = result
        except Exception as e:
            print(f"RackVirtual get went wrong: {e}")

        return data

    def insert(self, body):
        data = ""
        try:
            new_id = self.get()[-1]['code'] + 1
            transition = f"{body['translation'][0]}/{body['translation'][1]}/{body['translation'][2]}"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO racks_virtual (code, depth, shelf_width, shelf_height, columns_amount, "
                           f"rows_amount, border_width, color, translation, free_space_x, free_space_y) "
                           f"VALUES ({new_id}, {body['depth']}, {body['shelf_width']}, {body['shelf_height']}, "
                           f"{body['columns_amount']}, {body['rows_amount']}, {body['border_width']},"
                           f"'{body['color']}', {transition}, {body['free_space_x']}, {body['free_space_y']})")
            print(f'RackVirtual insert res {new_id}')
            data = new_id
        except Exception as e:
            print(f"RackVirtual insert went wrong: {e}")

        return data

    def update(self, id, body):
        data = ""
        try:
            new_id = self.get()[-1]['code'] + 1
            transition = f"{body['translation'][0]}/{body['translation'][1]}/{body['translation'][2]}"
            cursor = connection.cursor()
            cursor.execute(f"UPDATE racks_virtual SET depth={body['depth']}, shelf_width={body['shelf_width']}, "
                           f"shelf_height={body['shelf_height']}, columns_amount={body['columns_amount']}, "
                           f"rows_amount={body['rows_amount']}, border_width={body['border_width']}, "
                           f"color='{body['color']}', translation={transition}, free_space_x={body['free_space_x']}, "
                           f"free_space_y={body['free_space_y']} WHERE code={id}")
            print(f'RackVirtual update res {new_id}')
            data = new_id
        except Exception as e:
            print(f"RackVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE from racks_virtual WHERE code={id}')
            print(f'RackVirtual delete res {data}')
            data = data
        except Exception as e:
            print(f"RackVirtual delete went wrong: {e}")

        return data