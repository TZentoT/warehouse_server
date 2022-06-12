import json

from django.db import models, connection
from django.core import serializers

from Services.converters import json_converter
from .shelf_virtual import ShelfVirtual
from .rack import Rack

class RackVirtual(models.Model):

    def get(self, code=-1):
        data = []
        try:
            cursor = connection.cursor()
            if code == -1:
                cursor.execute("SELECT * FROM racks_virtual ORDER BY code ASC")
            if code != -1:
                cursor.execute(f"SELECT * FROM racks_virtual WHERE  code={code}")
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
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO racks_virtual (code, depth, shelf_width, shelf_height, columns_amount, "
                           f"rows_amount, border_width, color, translation, free_space_x, free_space_y) "
                           f"VALUES ({data['id']}, {data['depth']}, {data['shelf_width']}, {data['shelf_height']}, "
                           f"{data['columns_amount']}, {data['rows_amount']}, {data['border_width']},"
                           f"'{data['color']}', '{data['translation']}', {data['free_space_x']}, {data['free_space_y']})")
            self.insert_new_shelves(data)
            print(f'RackVirtual insert res {data}')
        except Exception as e:
            print(f"RackVirtual insert went wrong: {e}")

        return data

    def update(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            cur_rack = self.get(data['id'])[0]
            cursor = connection.cursor()
            if data['columns_amount'] != cur_rack['columns_amount'] or cur_rack['rows_amount'] != data['rows_amount']:
                self.insert_new_shelves(data)
                cursor.execute(f"UPDATE racks_virtual SET depth={data['depth']}, shelf_width={data['shelf_width']}, "
                               f"shelf_height={data['shelf_height']}, columns_amount={data['columns_amount']}, "
                               f"rows_amount={data['rows_amount']}, border_width={data['border_width']}, "
                               f"color='{data['color']}', translation='{data['translation']}', "
                               f"free_space_x={data['free_space_x']}, "
                               f"free_space_y={data['free_space_y']} WHERE code={data['id']}")
            else:
                ShelfVirtual().update({}, data['lifting_capacity'], data['id'])
                cursor.execute(f"UPDATE racks_virtual SET depth={data['depth']}, shelf_width={data['shelf_width']}, "
                               f"shelf_height={data['shelf_height']}, border_width={data['border_width']}, "
                               f"color='{data['color']}', translation='{data['translation']}', "
                               f"free_space_x={data['free_space_x']}, free_space_y={data['free_space_y']}"
                               f"WHERE code={data['id']}")
            print(f"RackVirtual update res {data}")
        except Exception as e:
            print(f"RackVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = id
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            is_possible_to_delete = True
            racks = Rack().get_rack("", 0, 0, data['id'])
            if len(racks) != 0:
                is_possible_to_delete = False

            if is_possible_to_delete :
                ShelfVirtual().delete(data['id'])
                cursor = connection.cursor()
                cursor.execute(f"DELETE from racks_virtual WHERE code={data['id']}")
                print(f"RackVirtual delete res {data}")
                data = "Тип стеллажа успеношно удален"
            else:
                data = "Невозможно удалить. Некоторые стеллажы привязаны к данному типу стеллажа"
        except Exception as e:
            print(f"RackVirtual delete went wrong: {e}")

        return data

    def insert_new_shelves(self, data):
        rack_id = data['id']
        capacity = data['lifting_capacity']
        rows = data['rows_amount']
        columns = data['columns_amount']
        print(data)
        ShelfVirtual().delete(rack_id)
        iterator = 1
        for i in range(rows):
            for j in range(columns):
                body = {
                    'rack_id': rack_id,
                    'column': j,
                    'row': i,
                    'lifting_capacity': capacity,
                    'name': f"Полка {iterator}"
                }
                ShelfVirtual().insert(body)
                print('insert_new_shelves success')
                iterator += 1
        return 0