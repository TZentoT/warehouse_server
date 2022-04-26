
from django.db import models, connection


class GoodType(models.Model):

    def get_good_types(self):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM goods_type ORDER BY code ASC")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'article', 'category', 'subcategory_2', 'subcategory_3', 'subcategory_4',
                    'absolute_path', 'price', 'price_old', 'price_buy', 'amount', 'amount_ordered', 'amount_limit',
                    'description', 'description_short', 'specifications', 'brand', 'weight', 'color', 'photo',
                    'photo_path', 'status', 'warranty')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'res {data}')
        except Exception as e:
            print(f"get_good_types went wrong: {e}")

        return data


