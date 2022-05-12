from django.db import models, connection


class Subcategories4(models.Model):

    def get_categories(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM goods_subcategories_4 ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name')
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result

        except Exception as e:
            print(f"Smth wrong: {e}")

        return data
