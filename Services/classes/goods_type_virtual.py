import json

from django.db import models, connection

from Services.converters import json_converter

from .good_type import GoodType


class GoodsTypeVirtual(models.Model):

    def get(self):
        data = []
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM goods_type_virtual ORDER BY id ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('id', 'width', 'height', 'depth', 'color', 'translation', 'name')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'GoodsTypeVirtual get res {result}')
            data = result

        except Exception as e:
            print(f"GoodsTypeVirtual get went wrong: {e}")

        return data

    def insert(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO goods_type_virtual (id, width, height, depth, color, translation, name)"
                           f"VALUES ({data['id']}, {data['width']}, {data['height']}, {data['depth']}, "
                           f"'{data['color']}', '{data['translation']}', '{data['name']}')")
            print(f'GoodsTypeVirtual insert res {data}')
        except Exception as e:
            print(f"GoodsTypeVirtual insert went wrong: {e}")

        return data

    def update(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE goods_type_virtual SET width={data['width']}, height={data['height']}, "
                           f"depth={data['depth']}, color='{data['color']}', name='{data['good_name']}', "
                           f"translation='{data['translation']}' WHERE id={data['id']}")
            print(f'GoodsTypeVirtual update res {data}')
        except Exception as e:
            print(f"GoodsTypeVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = id
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        try:
            is_possible_to_delete = True
            goods_type = GoodType().get_good_types()
            for good_type in goods_type:
                if good_type['virtual_type'] == data['id']:
                    is_possible_to_delete = False
            if is_possible_to_delete:
                cursor = connection.cursor()
                cursor.execute(f"DELETE from goods_type_virtual WHERE id={data['id']}")
                print(f'GoodsTypeVirtual delete res {data}')
                data = "Тип товара успешно удален"
            else:
                data = "Невозможно удалить. Некоторые товары привязаны к данному типу товара"
        except Exception as e:
            print(f"GoodsTypeVirtual delete went wrong: {e}")

        return data