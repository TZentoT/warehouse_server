import json

from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async

from Services.converters import json_converter


class ShelfVirtual(models.Model):

    def get(self, rack_id=-1):
        data = []
        try:
            cursor = connection.cursor()
            if rack_id == -1:
                cursor.execute(f"SELECT * FROM shelfs_virtual ORDER BY code ASC")
            if rack_id != -1:
                cursor.execute(f"SELECT * FROM shelfs_virtual WHERE rack_id={rack_id} ORDER BY code ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'lifting_capacity', 'row', 'column', "rack_id")
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f"ShelfVirtual get res {result}")
            data = result
        except Exception as e:
            print(f"ShelfVirtual get went wrong: {e}")

        return data

    def insert(self, body):
        data = body
        print('data')
        print(f"{data}")
        try:
            new_id = 1
            if len(self.get()) != 0:
                new_id = self.get()[-1]['code'] + 1
            print(new_id)
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shelfs_virtual "
                           f"VALUES ({new_id}, '{data['name']}', {data['lifting_capacity']}, "
                           f"{data['row']}, {data['column']}, {data['rack_id']})")
            print(f"ShelfVirtual insert res {new_id}")
            data = new_id
        except Exception as e:
            print(f"ShelfVirtual insert went wrong: {e}")

        return data

    def update(self, body={}, capacity=0, rack_id=0):
        data = body
        if body != {}:
            data = json.loads(data)
            data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            if body != {} and capacity == 0 and rack_id == 0:
                cursor.execute(f"UPDATE shelfs_virtual SET lifting_capacity={data['lifting_capacity']}"
                               f" WHERE rack_id={data['id']}")
            if body == {} and capacity != 0 and rack_id != 0:
                cursor.execute(
                    f"UPDATE shelfs_virtual SET lifting_capacity={capacity} WHERE rack_id={rack_id}")
            print(f"ShelfVirtual update res {data}")
        except Exception as e:
            print(f"ShelfVirtual update went wrong: {e}")

        return data

    def delete(self, id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"DELETE from shelfs_virtual WHERE rack_id={id}")
            print(f"ShelfVirtual delete res {data}")
            data = data
        except Exception as e:
            print(f"ShelfVirtual delete went wrong: {e}")

        return data