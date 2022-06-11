
from django.db import models, connection
from .subcategories_2 import Subcategories2
from .subcategories_3 import Subcategories3
from .categories import Categories

class GoodType(models.Model):

    def get_good_types(self, code=-1):
        data = []
        try:
            cursor = connection.cursor()
            if code == -1:
                cursor.execute(f"SELECT * FROM goods_type ORDER BY code ASC")
            if code != -1:
                cursor.execute(f"SELECT * FROM goods_type WHERE code={code}")
            rows = cursor.fetchall()
            result = []
            keys = ('code', 'name', 'article', 'category', 'subcategory_2', 'subcategory_3', 'subcategory_4',
                    'absolute_path', 'price', 'price_old', 'price_buy', 'amount', 'amount_ordered', 'amount_limit',
                    'description', 'description_short', 'specifications', 'brand', 'weight', 'color', 'photo',
                    'photo_path', 'status', 'warranty', 'virtual_type')
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
            print(f'get_good_types {data}')
        except Exception as e:
            print(f"get_good_types went wrong: {e}")

        return data

    def get_good_types_with_cats(self):
        data = ""
        try:
            goods = self.get_good_types()
            subcategories = Subcategories3().get_subcategories()
            categories = Subcategories2().get_subcategories()

            for element in goods:
                for category in categories:
                    if category['code'] == element['subcategory_2']:
                        element['subcategory_2'] = category['name']
                for subcategory in subcategories:
                    if subcategory['code'] == element['subcategory_3']:
                        element['subcategory_3'] = subcategory['name']
            data = goods
            print(f'res {data}')
        except Exception as e:
            print(f"get_good_types went wrong: {e}")

        return data

    def update(self, amount, code):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE goods_type SET amount=amount - {amount} WHERE code={code}")
        except Exception as e:
            print(f"get_good_types went wrong: {e}")

        return data

