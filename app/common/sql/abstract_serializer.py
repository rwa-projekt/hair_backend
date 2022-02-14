from ast import arg
from app.common.constants import *

class AbstractSqlSerializer:
    """
    1. Table name
    Uz String za naziv dodat |
    """
    table = ''
    string_fields = ''
    fields = []
    json_fields = ''
    key_value = ''
    json_build_object_fields = []
    
    def __init__(self, *args, **kwargs) -> None:
        self.reset()
        if len(args) >= 1:
            self.table = args[0]
        print(self.table)


    def reset(self):
        self.fields = []
        self.string_fields = ''
        self.table = ''
        self.json_fields = ''
        self.key_value = ''
        self.json_build_object_fields = []

    def fields_to_string(self):
        print(self.table)
        print(self.fields)
        if not self: return NULL
        for field in self.fields:
            if field[0] != '(':
                self.string_fields += f'{self.table}."{self.get_column_name(field)}" as {self.get_field_name(field)},'
            else:
                self.string_fields += f'{self.get_column_name(field)} as {self.get_field_name(field)},'
        
        print("KEY VALUE: ")
        print(self.key_value)
        for field in self.json_build_object_fields:
            if 'column' in field and field['column']:
                self.key_value += f"""
                    case
                        when {self.table}.{field['column']} is null then
                            null
                        else
                            JSON_BUILD_OBJECT (
                                {field['object'].get_key_value()}
                            )
                    end {field['name']},
                """
            else:
                self.key_value += f"""
                    JSON_BUILD_OBJECT (
                        {field['object'].get_key_value()}
                    ) {field['name']},
                """
        print(self.key_value)
        if self.key_value:
            self.string_fields += self.key_value

        self.string_fields = self.string_fields.strip()[:-1]
        print(self.string_fields)
        return self.string_fields

    def get_field_name(self, field):
        arr = field.split('|')
        if len(arr) > 1:
            return arr[1]
        return field

    def get_column_name(self, field):
        return field.split('|')[0]
    
    def get_key_value(self):
        for field in self.fields:
            if field[0] != '(':
                self.key_value += f"'{self.get_field_name(field)}', {self.table}.\"{self.get_column_name(field)}\","
            else:
                self.key_value += f"'{self.get_field_name(field)}', {self.get_column_name(field)},"
        for field in self.json_build_object_fields:
            self.key_value += f"""
                '{field['name']}', JSON_BUILD_OBJECT (
                    {field['object'].get_key_value()}
                ),
            """
        self.key_value = self.key_value.strip()[:-1]
        return self.key_value

    def fields_to_json(self, name=None, array=False):
        if not array:
            self.json_fields = f"""
                JSON_BUILD_OBJECT (
                    {self.get_key_value()}
                ) as {name}
            """
        else:
            self.json_fields = f"""
                ARRAY_AGG(
                   JSON_BUILD_OBJECT (
                    {self.get_key_value()}
                    ) 
                ) as {name}
            """
        return self.json_fields
