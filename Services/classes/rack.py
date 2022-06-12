import json

from django.db import models, connection
from django.core import serializers

from asgiref.sync import sync_to_async

from Services.converters import json_converter
from .shelf import Shelf
from .shelf_virtual import ShelfVirtual

class Rack(models.Model):

    def get_rack(self, name="", zone_num=0, code=0, rack_id=-1):
        data = []
        try:
            cursor = connection.cursor()
            if name == "" and zone_num == 0 and code == 0 and rack_id == -1:
                cursor.execute('SELECT * FROM racks ORDER BY code ASC')
            if name != "" and zone_num != 0 and code == 0 and rack_id == -1:
                cursor.execute(f"SELECT * FROM racks WHERE name LIKE '{name}' and zone_num={zone_num} ")
            if name == "" and zone_num != 0 and code == 0 and rack_id == -1:
                cursor.execute(f"SELECT * FROM racks WHERE zone_num={zone_num} ")
            if name == "" and zone_num == 0 and code != 0 and rack_id == -1:
                cursor.execute(f"SELECT * FROM racks WHERE code={code} ")
            if name == "" and zone_num == 0 and code == 0 and rack_id != -1:
                cursor.execute(f"SELECT * FROM racks WHERE rack_type_id={rack_id} ")
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
            cur_racks_in_zone = self.get_rack("", data['zone_num'])

            rack_num = 1
            if len(cur_racks_in_zone) != 0:
                rack_num = len(cur_racks_in_zone)+1

            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO racks (code, name, racks_num, zone_num, center_point, rotation, "
                           f"rack_type_id, type)"
                           f"VALUES ({data['id']}, '{data['name']}', {rack_num}, '{data['zone_num']}', "
                           f"'{data['center_point']}', '{data['rotation']}', '{data['rack_type_id']}', "
                           f"'{data['type']}')")

            print(f"Rack insert res {data['id']}")
            self.insert_new_shelves(data['rack_type_id'], data['id'])
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
            cur_rack = self.get_rack("", 0, data['id'])[0]

            if data['rack_type_id'] == cur_rack['rack_type_id']:
                cursor.execute(f"UPDATE racks SET name='{data['name']}', center_point='{data['center_point']}', "
                           f"rotation='{data['rotation']}' WHERE code={data['id']}")
            else:
                Shelf().delete({}, data['id'])
                self.insert_new_shelves(data['rack_type_id'], data['id'])
                cursor.execute(f"UPDATE racks SET name='{data['name']}', center_point='{data['center_point']}', "
                               f"rotation='{data['rotation']}', rack_type_id={data['rack_type_id']} "
                               f"WHERE code={data['id']}")

            print(f"Rack update res {data}")
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
                Shelf().delete({}, data['id'])
                cursor.execute(f"DELETE from racks WHERE code={data['id']}")
            if id != -1:
                racks = self.get_rack("", id)
                for rack in racks:
                    Shelf().delete({}, rack['code'])
                cursor.execute(f"DELETE from racks WHERE zone_num={id}")
            print(f"Rack delete res {data}")
            data = data
        except Exception as e:
            print(f"Rack delete went wrong: {e}")

        return data

    def insert_new_shelves(self, rack_type, rack_num):
        virtual_shelves = ShelfVirtual().get(rack_type)
        new_id_shelf = 1
        shelves = Shelf().get_shelfs()
        if len(shelves) != 0:
            new_id_shelf = shelves[-1]['code'] + 1

        iterator = 1
        for shelf in virtual_shelves:
            body = {
                'id': new_id_shelf,
                'name': f"Полка {iterator}",
                'shelf_num': iterator,
                'rack_num': rack_num,
                'capacity': shelf['lifting_capacity']
            }
            Shelf().insert(json.dumps(body))
            iterator += 1
            new_id_shelf += 1

        return 0
