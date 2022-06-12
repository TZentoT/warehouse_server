import json

from django.db import models, connection

from Services.converters import json_converter


class Shelf(models.Model):

    def get_shelfs(self, name="", rack_num=0):
        data = []
        try:
            cursor = connection.cursor()
            if name == "" and rack_num == 0:
                cursor.execute('SELECT * FROM shelfs ORDER BY code ASC')
            if name != "" and rack_num != 0:
                cursor.execute(f"SELECT * FROM shelfs WHERE name LIKE '{name}' and rack_num={rack_num}")
            if name == "" and rack_num != 0:
                cursor.execute(f"SELECT * FROM shelfs WHERE rack_num={rack_num}")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'shelf_num', 'rack_num', 'capacity', 'shelf_space')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'Shelf get_shelfs res {result}')
            data = result

        except Exception as e:
            print(f"Shelf get_shelfs went wrong: {e}")

        return data

    def insert(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        print(f"Shelf insert {data}")
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shelfs (code, name, shelf_num, rack_num, capacity) "
                           f"VALUES ({data['id']}, '{data['name']}', {data['shelf_num']}, '{data['rack_num']}', "
                           f"'{data['capacity']}')")
            print(f"Shelf insert res {data['id']}")

        except Exception as e:
            print(f"Shelf insert went wrong: {e}")

        return data

    def update(self, body):
        data = body
        data = json.loads(data)
        data = json_converter.JsonConverter().convert(data)
        print(f"Shelf update {data}")
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE shelfs SET name='{data['name']}', shelf_num='{data['shelf_num']}', "
                           f"rack_num='{data['rack_num']}', capacity='{data['capacity']}' WHERE rack_num={data['id']}")
            print(f'Shelf update res {data}')
        except Exception as e:
            print(f"Shelf update went wrong: {e}")

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
                cursor.execute(f"DELETE from shelfs WHERE rack_num={data['id']}")
            if id != -1:
                cursor.execute(f"DELETE from shelfs WHERE rack_num={id}")
            print(f'Shelf delete res {data}')
        except Exception as e:
            print(f"Shelf delete went wrong: {e}")

        return data