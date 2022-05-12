from django.db import models, connection


class ShelfSpace(models.Model):

    def get_shelf_space(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM shelf_space ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'good', 'amount', 'shelf_num', 'status')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result

        except Exception as e:
            print(f"get_shelf_space went wrong: {e}")

        return data

    def insert(self, good, amount, shelf_num):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO shelf_space (good, amount, shelf_num) VALUES "
                           f"({good}, {amount}, {shelf_num})")

        except Exception as e:
            print(f"Smth wrong: {e}")

        return data

    def update(self, shelf_num, code):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE shelf_space SET shelf_num={shelf_num} WHERE code={code}")

        except Exception as e:
            print(f"Smth wrong: {e}")

        return data
