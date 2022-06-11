from django.db import models, connection


class Color(models.Model):

    def get_color(self):
        data = []
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT id,name FROM colors ORDER BY id ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('id', 'name')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result

        except Exception as e:
            print(f"Smth wrong: {e}")

        return data
