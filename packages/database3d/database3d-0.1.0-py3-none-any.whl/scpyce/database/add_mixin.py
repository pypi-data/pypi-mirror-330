"""
Description
"""

import warnings
import sqlite3
import numpy as np
import datetime
import json
from collections.abc import Iterable


class WriteMixin:

    def add_log(self, event_message):
        """
        Logs a model event.
        
        Parameters:
        None

        Returns:
        None
        """     

        cur = self.connection.cursor()

        version_query = """
        INSERT INTO model_log (
            version,
            user, 
            date,
            event) 
            VALUES 
            (?,?,?,?)
            """
        version_value_string = (self.version,
                                self.user,
                                datetime.datetime.now(),
                                event_message
                                )

        cur.execute(version_query, version_value_string)

        self.connection.commit()

        cur.close()

    
    def add(self, model_object):
        
        object_id = None
        table_name = model_object.__class__.__name__.lower()
        attribute_dictionary = model_object.__dict__

        self.build_table(model_object)

        attribute_names = ','.join([attribute_name.lower()  for attribute_name in attribute_dictionary.keys()])

        query = f'INSERT INTO {table_name} ({attribute_names})VALUES({'?,'*(len(attribute_dictionary.keys())-1)}?)'
        values = []

        for attribute in attribute_dictionary.items():

            attribute_name = attribute[0]
            attribute_value = attribute[1]

            if attribute_name == '_id':
                
                object_id = attribute_value

                check_query = f'SELECT _id FROM {table_name} WHERE (_id = ?)'
                check_result = self.cursor.execute(check_query, [object_id]).fetchone()

                if check_result is not None:
                    return object_id

            if (not isinstance(attribute_value, int) and 
                not isinstance(attribute_value, float) and 
                not isinstance(attribute_value, str) and
                not isinstance(attribute_value, bool)
                ):

                if isinstance(attribute_value, Iterable):
                    attribute_value = json.dumps(attribute_value)
                else:
                    attribute_value = self.add(attribute_value)
            
            values.append(attribute_value)
                
        self.cursor.execute(query, values)

        if object_id == None:
            object_id = self.cursor.lastrowid
        
        self.events.append(f'added: {table_name} id = {object_id}')

        return object_id
        






