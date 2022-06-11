from django.db import models, connection


class GoodsTypeVirtual(models.Model):

    def get(self):
        data = []
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM goods_type_virtual ORDER BY id ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('id', 'width', 'height', 'depth', 'color', 'translation')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'GoodsTypeVirtual get res {result}')
            data = result

        except Exception as e:
            print(f"GoodsTypeVirtual get went wrong: {e}")

        return data

    def insert(self, body):
        data = ""
        try:
            new_id = self.get()[-1]['id'] + 1
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO goods_type_virtual (id, width, height, depth, color, translation)"
                           f"VALUES ({new_id}, {body['width']}, {body['height']}, {body['depth']}, "
                           f"{body['color']}, {body['translation']})")
            print(f'GoodsTypeVirtual insert res {new_id}')
            data = new_id
        except Exception as e:
            print(f"GoodsTypeVirtual insert went wrong: {e}")

        return data

    def update(self, id, body):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE goods_type_virtual SET width={body['width']}, height={body['height']}, "
                           f"depth={body['depth']}, color={body['color']}, "
                           f"translation={body['translation']} WHERE id={id}")
            print(f'GoodsTypeVirtual update res {data}')
        except Exception as e:
            print(f"GoodsTypeVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE from goods_type_virtual WHERE id={id}')
            print(f'GoodsTypeVirtual delete res {data}')
            data = data
        except Exception as e:
            print(f"GoodsTypeVirtual delete went wrong: {e}")

        return data