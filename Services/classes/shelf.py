from django.db import models, connection


class Shelf(models.Model):

    def get_shelfs(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM shelfs ORDER BY code ASC')
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
