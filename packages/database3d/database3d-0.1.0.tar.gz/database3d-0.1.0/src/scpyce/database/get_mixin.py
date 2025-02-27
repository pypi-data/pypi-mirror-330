"""
Contains functions for reading information from the SQLite database model.
"""
import sqlite3
import numpy as np

from ..objects import properties # pylint: disable=import-error
from ..objects import element # pylint: disable=import-error
from ..objects import load  # pylint: disable=import-error

class ReadMixin:

    def get_version(self):
        
        result = self.cursor.execute("SELECT * FROM model_info").fetchall()

        if len(result) == 0:
            return '0.0.0'

        return result[-1][0]


    def get_material(self, material_name):
        """ 
        Gets a material object from the SQLite database tables based on a material name reference.

        Parameters:
        material_name (string): The name of the material to retreive from the database.

        Returns:
        material object: The retreived material. 
        """

        material_data = self.cursor.execute("SELECT * FROM property_material WHERE _id = ?",[material_name]).fetchone()
        material_object = properties.Material(*material_data)

        return material_object

    def get_section(self, section_name):
        """ 
        Gets a section object from the SQLite database tables based on a section name reference.

        Parameters:
        section_name (string): The name of the section to retreive from the database.

        Returns:
        section object: The retreived section. 
        """
        section_data = self.cursor.execute("SELECT * FROM property_section WHERE _id = ?",[section_name]).fetchone()
        section_data = list(section_data)
        section_data[1] = self.get_material(section_data[1])
        section_object = properties.Section(*section_data)

        return section_object

    def get_node(self, node_index):
        """ 
        Gets a node object from the SQLite database tables based on a node index reference.

        Parameters:
        node_index (float): The index of the node to retreive from the database.

        Returns:
        node object: The retreived node.
        """
        node_data = self.cursor.execute("SELECT * FROM element_node LIMIT 1 OFFSET ?",[int(node_index)]).fetchone()

        node_object = element.Node(node_data[1],
                                    node_data[2],
                                    node_data[3],
                                    node_data[4])


        return node_object

    def get_bar(self, bar_name):
        """ 
        Gets a bar object from the SQLite database tables based on a bar name reference.

        Parameters:
        bar_name (string): The name of the bar to retreive from the database.

        Returns:
        bar object: The retreived bar.  
        """

        bar_data = self.cursor.execute("SELECT * FROM element_bar WHERE _id = ?",[bar_name]).fetchone()
        bar_data = list(bar_data)

        id = bar_data[0]
        node_a = self.get_node(bar_data[1])
        node_b = self.get_node(bar_data[2])
        section = self.get_section(bar_data[3])

        orientation_vector = str.replace(bar_data[4],'[','')
        orientation_vector = str.replace(orientation_vector,']','')
        orientation_vector = str.split(orientation_vector,' ')

        orientation_vector = np.array([float(orientation_vector[0]),
                                        float(orientation_vector[1]),
                                        float(orientation_vector[2])]
                                        )

        release_a = bar_data[5]
        release_b = bar_data[6]

        bar_data = bar_data[7]

        bar_object = element.Bar(node_a,
                                    node_b,
                                    section,
                                    orientation_vector,
                                    release_a,
                                    release_b,
                                    id,
                                    bar_data)

        return bar_object

    def get_bars(self):
        """ 
        Gets a bar object from the SQLite database tables based on a bar name reference.

        Parameters:
        bar_name (string): The name of the bar to retreive from the database.

        Returns:
        bar object: The retreived bar.  
        """

        bar_data = self.cursor.execute("SELECT _id FROM element_bar")
        bar_id_list = list(bar_data)

        return [self.get_bar(id[0]) for id in bar_id_list]
    
    def get_node_displacements(self, node_id):

        node_result_data = self.cursor.execute("SELECT * FROM result_node_displacement WHERE node_index = ?",[node_id]).fetchone()
        node_result_data = list(node_result_data)

        ux = node_result_data[2]
        uy = node_result_data[3]
        uz = node_result_data[4]
        rx = node_result_data[5]
        ry = node_result_data[6]
        rz = node_result_data[7]

        return [ux, uy, uz, rx, ry, rz]


    def get_bar_displacements(self, bar_name):

        bar_data = self.cursor.execute("SELECT * FROM element_bar WHERE _id = ?",[bar_name]).fetchone()
        bar_data = list(bar_data)

        node_a_displacements = self.get_node_displacements(bar_data[1])
        node_b_displacements = self.get_node_displacements(bar_data[2])

        return [node_a_displacements, node_b_displacements]


    def get_support(self, node_index):

        support_data = (self.cursor.execute("SELECT * FROM element_support WHERE node_index = ?",[node_index])).fetchone()

        node = self.get_node(node_index)
        support = element.Support(node,
                                  support_data[1],
                                  support_data[2],
                                  support_data[3],
                                  support_data[4],
                                  support_data[5],
                                  support_data[6],
                                  support_data[7]
                                  )

        return support


    def get_supports(self):

        support_data = list(self.cursor.execute("SELECT * FROM element_support"))
        
        return [self.get_support(data[0]) for data in support_data]

    def get_point_load(self, node_index):

        load_data = (self.cursor.execute("SELECT * FROM load_pointload WHERE node_index = ?",[node_index])).fetchone()

        node = self.get_node(node_index)
        point_load = load.PointLoad(node,
                                    float(load_data[1]),
                                    float(load_data[2]),
                                    float(load_data[3]),
                                    float(load_data[4]),
                                    float(load_data[5]),
                                    float(load_data[6])
                                    )
        
        return point_load
    
    def get_point_loads(self):

        load_data = list(self.cursor.execute("SELECT * FROM load_pointload"))

        return [self.get_point_load(data[0]) for data in load_data]

    def get_node_count(self):

        query = f"SELECT COUNT(*) FROM element_node"

        return self.cursor.execute(query).fetchone()[0]
    
    def get_bar_count(self):

        query = f"SELECT COUNT(*) FROM element_bar"

        return self.cursor.execute(query).fetchone()[0]

    def get_material_count(self):

        query = f"SELECT COUNT(*) FROM property_material"

        return self.cursor.execute(query).fetchone()[0]

    def get_section_count(self):

        query = f"SELECT COUNT(*) FROM property_section"

        return self.cursor.execute(query).fetchone()[0]

    def get_support_count(self):

        query = f"SELECT COUNT(*) FROM element_support"

        return self.cursor.execute(query).fetchone()[0]
    
    def get_pointload_count(self):

        query = f"SELECT COUNT(*) FROM load_pointload"

        return self.cursor.execute(query).fetchone()[0]

