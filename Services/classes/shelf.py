from django.db import models, connection


class Shelf(models.Model):

    def get_shelfs(self, name="", rack_num=0):
        data = ""
        try:
            cursor = connection.cursor()
            if name == "" and rack_num == 0:
                cursor.execute('SELECT * FROM shelfs ORDER BY code ASC')
            if name != "" and rack_num != 0:
                cursor.execute(f"SELECT * FROM shelfs WHERE name LIKE '{name}' and rack_num={rack_num}")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'shelf_num', 'rack_num', 'capacity', 'shelf_space')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result

        except Exception as e:
            print(f"Smth wrong: {e}")

        return data
