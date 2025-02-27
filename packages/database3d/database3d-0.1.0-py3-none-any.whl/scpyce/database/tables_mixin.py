"""
Containse the functions for building the tables in the SQLite database model.
"""
import sqlite3
from collections.abc import Iterable

class TablesMixin:

    def build_tables(self):
        """
        Creates the following tables for the SQLite database model: 

        - model_info
        - model_log

        Parameters:
        None

        Returns:
        None
        """

        #Build object tables
        self.build_info_table()
        self.build_log_table()
       
    
    def clear_all_tables(self):

        tables = self.get_tables()
        for table, in tables:
            #self.cursor.execute(f"DROP TABLE {table};")
            self.cursor.execute(f"DELETE FROM {table}")
        


    def get_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_schema WHERE type='table';")
        tables = self.cursor.fetchall()
        return tables

    def build_info_table(self):

        # create the database table if it doesn't exist
        info_table_schema = """
        CREATE TABLE IF NOT EXISTS model_info (
            version TEXT PRIMARY KEY,
            user TEXT NOT NULL,
            date timestamp NOT NULL,
            nodes INTEGER NOT NULL,
            bars INTEGER NOT NULL,
            sections INTEGER NOT NULL,
            materials INTEGER NOT NULL,
            loads INTEGER NOT NULL,
            supports INTEGER NOT NULL,
            errors TEXT,
            warnings TEXT,
            run_time FLOAT NOT NULL
            );
        """
        self.cursor.execute(info_table_schema)


    def build_log_table(self):

        # create the database table if it doesn't exist
        table_schema = """
        CREATE TABLE IF NOT EXISTS model_log (
            version TEXT NOT NULL,
            user TEXT NOT NULL,
            date timestamp NOT NULL,
            event TEXT NOT NULL
            );
        """
        self.cursor.execute(table_schema)


    def build_table(self, model_object):

        table_name = model_object.__class__.__name__
        attribute_string = 'value TEXT'
        table_type = 'object' #TODO add to table name

        if hasattr(model_object, 'type'):
            table_type = str(model_object.type)

        if hasattr(model_object, '__dict__') and len(model_object.__dict__) > 0:
            attribute_dictionary = model_object.__dict__
            attribute_string_list = []

            for attribute in attribute_dictionary.items():

                attribute_name = attribute[0].lower()
                attribute_value = attribute[1]
                attribute_value_type = 'NULL'
                primary_key = ''

                if isinstance(attribute_value, int):
                    attribute_value_type = 'INTEGER'
                elif isinstance(attribute_value, float):
                    attribute_value_type = 'FLOAT'
                elif isinstance(attribute_value, str):
                    attribute_value_type = 'TEXT'
                elif isinstance(attribute_value, bool):
                    attribute_value_type = 'BOOL'
                elif isinstance(attribute_value, Iterable):
                    attribute_value_type = 'TEXT'
                else:
                    self.build_table(attribute_value)
                    attribute_value_type = 'INTEGER'
                
                #TODO add table or lists
                
                if attribute_name == '_id':
                    primary_key = ' NOT NULL PRIMARY KEY'


                attribute_string_list.append(f'{attribute_name} {attribute_value_type}{primary_key}')
            
            attribute_string = ','.join(attribute_string_list)
        
        table_schema = f'CREATE TABLE IF NOT EXISTS {table_name.lower()} (' + attribute_string + ');'

        self.cursor.execute(table_schema)
