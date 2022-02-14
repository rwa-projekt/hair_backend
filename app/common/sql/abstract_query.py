from re import S
from django.db import connection
from sqlparse import sql
from app.common.constants import *
from app.errors.services import trigger_django_404

class AbstractQuery:
    BEGIN_ARR = []
    BEGIN_STR = ''
    JOIN_ARR = []
    JOIN_STR = ''
    WHERE_ARR = []
    WHERE_STR = ''
    GROUP_BY_STR = ''
    ORDER_BY_STR = ''
    ORDERING = ASC
    LIMIT_STR = ''
    HAVING_STR = ''
    QUERY = """"""

    query_params = {}
    params = {}
    sql_data = None
    res = None
    error_msg = ''
    
    response_type = 'json'

    token = None
    user = None
    pk = None

    LOAD_MORE = False
    _next = None

    check_ser = None
    output_ser = None

    FINAL_RES = None

    def __init__(self, *args, **kwargs) -> None:
        self.reset()
        if 'query_params' in kwargs:
            self.query_params = kwargs.get('query_params')
            self.get_parameters()

        if CHECK_SERIALIZER in kwargs:
            self.check_ser = kwargs.get(CHECK_SERIALIZER)

        if OUTPUT_CHECK_SERIALIZER in kwargs:
            self.output_ser = kwargs.get(OUTPUT_CHECK_SERIALIZER)

        if 'token' in kwargs:
            self.token = kwargs.get('token')

        if 'pk' in kwargs:
            self.pk = kwargs.get('pk')
            self.params['pk'] = self.pk

        if 'load_more' in kwargs:
            self.LOAD_MORE = kwargs.get('load_more')

        if 'user' in kwargs:
            self.user = kwargs.get('user')

        if LIMIT in self.params:
            self.params[LIMIT] = int(self.params[LIMIT]) + 1

        self.check_params()



    def reset(self):
        self.BEGIN_ARR = []
        self.BEGIN_STR = ''
        self.JOIN_ARR = []
        self.JOIN_STRING = ''
        self.WHERE_ARR = []
        self.WHERE_STR = ''
        self.GROUP_BY_STR = ''
        self.ORDER_BY_STR = ''
        self.ORDERING = ASC
        self.LIMIT_STR = ''
        self.HAVING_STR = ''
        self.QUERY = """"""
        self.query_params = {}
        self.params = {}
        self.sql_data = None
        self.response_type = 'json'
        self.res = None
        self.error_msg = ''
        self.token = None
        self.user = None
        self.pk = None
        self._next = None
        self.LOAD_MORE = False
        self.FINAL_RES = dict(results = [], message = self.error_msg)
        self.check_ser = None
        self.output_ser = None
        
    def get_parameters(self):
        self.params = {}
        print(self.query_params)
        passed = []
        for key, value in self.query_params.items():
            if value:
                self.params[key] = value
                passed.append(key)
        # self.params['limit'] = 30 + 1
        return self.params

    def check_params(self):
        if self.check_ser:
            print("Provjera podataka...")
            ser = self.check_ser(data = self.params)
            ser.is_valid(raise_exception=True)
        return True

    def get_join_string(self) -> str:
        if not self.JOIN_ARR: return ''
        for i in self.JOIN_ARR:
            self.JOIN_STR += i + ' '

        return self.JOIN_STR

    def get_where_string(self) -> str:
        if not self.WHERE_ARR: return ''
        for count, i in enumerate(self.WHERE_ARR):
            if count < len(self.WHERE_ARR) - 1:
                self.WHERE_STR += i + ' and '
            else:
                self.WHERE_STR += i

        if self.WHERE_STR:
            self.WHERE_STR = 'WHERE ' + self.WHERE_STR

        return self.WHERE_STR

    def get_where_string_or(self) -> str:
        if not self.WHERE_ARR: return ''
        for count, i in enumerate(self.WHERE_ARR):
            if count < len(self.WHERE_ARR) - 1:
                self.WHERE_STR += i + ' or '
            else:
                self.WHERE_STR += i

        self.WHERE_STR = f'({self.WHERE_STR})'

        return self.WHERE_STR

    def get_begining_string(self):
        if not self.BEGIN_ARR: return ''
        self.BEGIN_STR = 'WITH RECURSIVE '
        for count, i in enumerate(self.BEGIN_ARR):
            if count <  len(self.BEGIN_ARR) - 1:
                self.BEGIN_STR += i + ', '
            else:
                self.BEGIN_STR += i
        return self.BEGIN_STR

    def get_bool_from_string(self, value):
        if value == '0': return False
        return True

    def format_ids(self, ids, delimeter='|'):
        if ids:
            ids = ids.replace(delimeter, ",")
            if ids[-1] == ',':
                ids = ids[:-1]
            ids = '(' + ids + ')'
            return ids
        return None

    def add_limit(self, value=None):
        if not value:
            self.LIMIT_STR = f'LIMIT {self.params.get(LIMIT, 20)}'
        else:
            self.LIMIT_STR = f'LIMIT {value}'


    def add_filter(self, column, arr, value):
        if column:
            if column in self.params:
                arr.append(value)
        else:
            arr.append(value)

    def add_group_by(self, value):
        if not self.GROUP_BY_STR:
            self.GROUP_BY_STR = f'GROUP BY {value} '
        else:
            self.GROUP_BY_STR = f', {value}'

    def add_order_by(self, value=None):
        if not value:
            if not self.ORDER_BY_STR:
                self.ORDER_BY_STR = f"ORDER BY {self.params.get(ORDER_BY, 'id')}"
            else:
                self.ORDER_BY_STR += f", {self.params.get(ORDER_BY, 'id')}"
        else:
            if not self.ORDER_BY_STR:
                self.ORDER_BY_STR = f'ORDER BY {value} '
            else:
                self.ORDER_BY_STR += f', {value}'

    def add_ordering(self, value=None):
        print("ORDERING:::: ")
        print(value)
        if not value:
            self.ORDERING = self.params.get(ORDERING, None)
        else:
            if value:
                if value.upper() in (ASC, DESC):
                    self.ORDERING = value.upper() 
        print(f"Self Ordering: {self.ORDERING}")

    def company_filter(self):
        if self.user:
            if self.user.company_id:
                self.add_filter(
                        None,
                        self.WHERE_ARR,
                        f'acc.company_id = {self.user.company_id}'
                    )
            else:
                self.add_filter(
                        None,
                        self.WHERE_ARR,
                        f'acc.company_id is null'
                    )
        

    def set_ordering(self):
        if self.ORDER_BY_STR and self.ORDERING and self.ORDERING.upper() in (ASC, DESC):
            self.ORDER_BY_STR += ' ' + self.ORDERING

    def add_account_asset_beginning_query_string(self):
        self.BEGIN_ARR.append(f"""
            account as (
                select user_id as account_id from authtoken_token where key = '{self.token}'
            ),
            account_assets as (
                select aaa.item_id from accounts_account_assets aaa where aaa.account_id = (select account_id from account)
                ),
            account_storage_children AS (
                    SELECT items_item.id
                    FROM items_item
                    WHERE id in ((select item_id from account_assets)) and is_active = true and is_warehouse = true
                    UNION
                    SELECT items_item.id
                    FROM items_item,account_storage_children
                    WHERE items_item.is_active = true and items_item.is_warehouse = true and items_item.parent_id = account_storage_children.id
                )
        """)

    def add_asset_beginning_query_string(self, asset_ids):
        if not asset_ids:
            return None
        self.BEGIN_ARR.append(f"""
            storage_children AS (
                    SELECT items_item.id
                    FROM items_item
                    WHERE id in {asset_ids} and is_active = true and is_warehouse = true
                    UNION
                    SELECT items_item.id
                    FROM items_item,storage_children
                    WHERE items_item.is_active = true and items_item.is_warehouse = true and items_item.parent_id = storage_children.id
                )
        """)


    def generate_sql(self):
        return self.QUERY

    def filter(self):
        return True

    def set_filters(self):
        if self.WHERE_ARR:
            self.WHERE_STR = self.get_where_string()
        if self.JOIN_ARR:
            self.JOIN_STR = self.get_join_string()
        if self.BEGIN_ARR:
            self.BEGIN_STR = self.get_begining_string()
        print(self.WHERE_STR)

    def check_output_data(self):
        if self.output_ser:
            print("Check output data...")
            if isinstance(self.res, list):
                if not self.output_ser(data=self.res, many=True).is_valid():
                    print("RESPONSE NOT OK.")
            else:
                if not self.output_ser(data=self.res, many=False).is_valid():
                    print("RESPONSE NOT OK.")

    def exec_query(self):
        self.prepare_exec()
        if not self.QUERY: 
            print("Nema queria")
            raise Exception
        try:
            with connection.cursor() as cursor:
                cursor.execute(self.QUERY)
                self.sql_data = cursor.fetchall()
        except Exception as e:
            print(str(e))
            raise Exception
        print(self.sql_data)

        if self.response_type != 'json':
            self.res = self.sql_data
            return self.res

        self.res = self.sql_data[0][0]

        if self.res == 404:
            raise trigger_django_404()

        self.check_output_data()
        return self.res

    def prepare_exec(self):
        self.filter()
        self.set_filters()
        self.set_ordering()
        self.generate_sql()

    def clear(self):
        pass

    def get_response(self):
        self.exec_query()
        self.clear()
        if self.LOAD_MORE:
            self.FINAL_RES['results'] = self.get_load_more_response()
        else:
            self.FINAL_RES['results'] = self.res
        return self.FINAL_RES
            
    def write_last_sql_query(self):
        print("Upisivanje posljednjeg querya...")
        f = open('last_sql.sql', 'w')
        f.write(self.QUERY)
        f.close()

    
    def get_load_more_response(self):

        if LIMIT in self.params and self.params[LIMIT]:
            print("Ima limit ")
            print(f"Duljina niza: {len(self.res)}")
            if len(self.res) >= int(self.params[LIMIT]):
                print("Duljina niza veca od limita.")
                del self.res[-1]
                if self.params.get(CURSOR, None):
                    self._next = ''
                    for c in self.params.get(CURSOR, '').split('|'):
                        print("KOLONA: ", c)
                        self._next += str(self.res[-1][c])
                # self._next = self.res[-1]['id']
            else: # Ako je povuceno manje elemenata od limita, svi su povuceni onda
                print("Duljina niza nije veca od limita")
                self._next = None
        else:
            print("Nema limit ili cursor")

        return {
            "cursor": {
                "next": self._next
            },
            "data": self.res
        }

    def get_next_column_name(self, tbl=None):
        columns = self.params.get(CURSOR).split('|')
        res = ''
        print(f"Splitted next cursor: {columns}")
        if len(columns) > 1:
            res = "CONCAT("
            if tbl:
                for c in columns:
                    res += f'{tbl}."{c}",'
            else:
                for c in columns:
                    res += f'"{c}",'
            res = res[:-1]
            res += ')'
        else:
            if tbl:
                res = f'{tbl}."{columns[0]}"'
            else:
                res = f'"{columns[0]}"'
        
        return res

    def set_next_condition(self, tbl=None):
        if NEXT and CURSOR in self.params:
            if self.ORDERING and self.ORDERING.upper() == DESC:
                self.add_filter(
                    NEXT,
                    self.WHERE_ARR,
                    f"{self.get_next_column_name(tbl)} < '{self.params.get(NEXT)}'"
                )
            else:
                self.add_filter(
                    NEXT,
                    self.WHERE_ARR,
                    f"{self.get_next_column_name(tbl)} > '{self.params.get(NEXT)}'"
                )