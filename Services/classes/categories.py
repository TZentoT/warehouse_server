from django.db import models, connection


class Categories(models.Model):

    def get_categories(self):
        data = []
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM goods_categories ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'status')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result

        except Exception as e:
            print(f"Smth wrong: {e}")

        return data
