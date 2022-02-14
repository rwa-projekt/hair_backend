from distutils.log import error
from django.db import transaction, connection
from rest_framework.exceptions import NotFound

from app.errors.services import trigger_exception

class SqlErrorCode:
    SQL_ERROR_CODES = {
        1000: {
            "msg": "Ne mozete prenijeti vecu kolicinu nego sto je na skladistu.",
            "code": 404
        },
        1001: {
            "msg": "Ne postoji dio.",
            "code": 404
        },
        1002: {
            "msg": "Ne postoji zahtjev za transport.",
            "code": 404
        },
        1003: {
            "msg": "email_exists",
            "code": 400
        },
        1111: {
            "msg": "object_not_exists",
            "code": 404
        }
    }

class Proc:
    proc_name = ''
    params = []
    response_type = 'json'

    def __init__(self, *args):
        if len(args) >= 1:
            self.proc_name = args[0]

            if len(args) >= 2:
                self.params = args[1]

                if len(args) >= 3:
                    self.response_type = args[2]

    def get_error_message(self, error_code):
        return SqlErrorCode.SQL_ERROR_CODES.get(error_code, 'Greska')

    def call(self):
        try:
            with connection.cursor() as cursor:
                cursor.callproc(self.proc_name, self.params)
                sql_data = cursor.fetchall()
        except Exception as e:
            print(str(e))
            raise trigger_exception(str(e), 500)
        # print(sql_data)
        if self.response_type == 'json':
            sql_data = sql_data[0][0]
        if sql_data == {} or sql_data == 404:
            raise NotFound        
        print(sql_data)
        if not isinstance(sql_data, int) and 'error_code' in sql_data:
            if sql_data['error_code'] >= 1000:
                msg = self.get_error_message(sql_data['error_code'])
                raise trigger_exception(msg['msg'], msg['code'])
            else:
                sql_data = []
        
        return sql_data


    def __str__(self):
        return f"{self.proc_name} - {self.params} - {self.response_type}"

    
    # @classmethod
    # def call(self, proc_name, params = [], response_type='json'):
    #     with connection.cursor() as cursor:
    #         cursor.callproc(proc_name, params)
    #         sql_data = cursor.fetchall()
    #     print(sql_data)
    #     if response_type == 'json':
    #         sql_data = sql_data[0][0]
    #     if sql_data == {}:
    #         raise NotFound
    #     return sql_data