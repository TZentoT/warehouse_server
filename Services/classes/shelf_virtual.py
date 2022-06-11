from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async


class ShelfVirtual(models.Model):

    def get(self):
        data = []
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM shelfs_virtual ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'lifting_capacity', 'row', 'column', "rack_id")
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'ShelfVirtual get res {result}')
            data = result
        except Exception as e:
            print(f"ShelfVirtual get went wrong: {e}")

        return data

    def insert(self, body):
        data = ""
        try:
            new_id = self.get()[-1]['code'] + 1
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shelfs_virtual (code, name, lifting_capacity, row, column, rack_id) "
                           f"VALUES ({new_id}, {body['name']}, {body['lifting_capacity']}, {body['row']}, "
                           f"{body['column']}, {body['rack_id']})")
            print(f'ShelfVirtual insert res {new_id}')
            data = new_id
        except Exception as e:
            print(f"ShelfVirtual insert went wrong: {e}")

        return data

    def update(self, id, body):
        data = ""
        try:
            new_id = self.get()[-1]['code'] + 1
            cursor = connection.cursor()
            cursor.execute(f"UPDATE shelfs_virtual SET name={body['name']}, lifting_capacity={body['lifting_capacity']},"
                           f"row={body['row']}, column={body['column']}, rack_id={body['rack_id']} WHERE code={id}")
            print(f'ShelfVirtual update res {new_id}')
            data = new_id
        except Exception as e:
            print(f"ShelfVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE from racks_virtual WHERE code={id}')
            print(f'ShelfVirtual delete res {data}')
            data = data
        except Exception as e:
            print(f"ShelfVirtual delete went wrong: {e}")

        return data