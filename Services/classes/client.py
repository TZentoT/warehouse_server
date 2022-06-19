import json

from django.db import models, connection
from django.core import serializers
from ..converters import json_converter


class Client(models.Model):

    def get_client(self):
        data = []
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM accounts ORDER BY code ASC')
            rows = cursor.fetchall()
            result = []
            keys = ("code", "name", "surname", "patronymic", "login", "password", "phone_num", "duty", "avatar")
            for row in rows:
                result.append(dict(zip(keys, row)))
            data = result
        except Exception as e:
            print(f"get_client went wrong: {e}")

        return data

    def insert_new_cliend(self, new_client):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO accounts (name, surname, patronymic, login, password, phone_num, duty) '
                           f'VALUES ({new_client["name"]}, {new_client["surname"]}, {new_client["patronymic"]}, '
                           f'{new_client["login"]}, {new_client["password"]}, {new_client["phone_num"]}, {new_client["duty"]})')
            rows = cursor.fetchall()
            result = []
            keys = ("code", "name", "surname", "patronymic", "avatar", "login", "password", "phone_num", "duty")
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result
        except Exception as e:
            print(f"insert_new_cliend went wrong: {e}")

        return data

    def update_existing_client(self, client):
        data = client
        # data = json.loads(data)
        # data = json_converter.JsonConverter().convert(data)
        try:
            cursor = connection.cursor()
            if data['duty'] != "":
                print(f"data: {client}")
                cursor.execute(f"UPDATE accounts SET name='{data['name']}', surname='{data['surname']}',"
                           f"patronymic='{data['patronymic']}', "
                           f"login='{data['login']}', password='{data['password']}', phone_num='{data['phone']}',"
                           f"duty='{data['duty']}' WHERE code={data['code']}")
            if data['duty'] == "":
                cursor.execute(f"UPDATE accounts SET name='{data['name']}', surname='{data['surname']}',"
                               f"patronymic='{data['patronymic']}', "
                               f"login='{data['login']}', password='{data['password']}', "
                               f"phone_num='{data['phone']}', avatar='{data['preview']}'"
                               f"WHERE code={data['code']}")

        except Exception as e:
            print(f"update_existing_client went wrong: {e}")

        return data

    def delete_existing_client(self, client):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM accounts WHERE code={client["code"]}')
        except Exception as e:
            print(f"delete_existing_client went wrong: {e}")

        return data

    def update_client_datatable(self, clients):
        datatable = clients
        datatable = json.loads(datatable)
        datatable = json_converter.JsonConverter().convert(datatable)

        accounts = self.get_client()
        accounts = json_converter.JsonConverter().convert(accounts)

        print(f'datatable: {datatable}')
        print(f'accounts: {accounts}')
        datatable_dump = []
        datatable_dump = datatable
        for account in accounts:
            # print(f'account: {account}')
            check = False
            for element in datatable:
                # print(f'elm: {element}')
                if account['code'] == element['code']:
                    check = True
                    self.update_existing_client(element)
                    print(f'datatable_dump: {datatable_dump}')
                    datatable_dump.remove(element)
                    print(f'datatable_dump: {datatable_dump}')

            if not check:
                self.delete_existing_client(account)

        if len(datatable_dump) > 0:
            for new_client in datatable_dump:
                self.insert_new_cliend(new_client)

        return b'Datatable updated'

    def get_img_avatar(self, id):
        data = ""
        try:
            cursor = connection.cursor()
            cursor.execute(f'SELECT avatar FROM accounts WHERE code={id}')
            rows = cursor.fetchall()
            result = []
            keys = ("avatar")
            for row in rows:
                result.append(dict(zip(keys, row)))
            print(f'res {result}')
            data = result
        except Exception as e:
            print(f"delete_existing_client went wrong: {e}")

        return data