"""
Contains the object classes for element objects of the structural model.
"""
import uuid
import numpy as np

from ..geometry import vector3d # pylint: disable=import-error
from ..geometry import plane # pylint: disable=import-error
from . import properties # pylint: disable=import-error

class ElementBase:

    def __init__(self, data_string=''):
        self.type = 'element'
        self.data = data_string


class Node(ElementBase):
    """
    Node object that represents a point in 3d space. 

    Parameters:
    x (float): The x coordinate of the node.
    y (float): The y coordinate of the node.
    z (float): The z coordinate of the node.

    Returns:
    Node object: Node object at the specified location.
    """

    def __init__(self,
                 x,
                 y,
                 z,
                 data = ''):

        self._id = f'{x}_{y}_{z}'
        self.x = x
        self.y = y
        self.z = z
        super().__init__(data)


    def to_string(self):
        """
        Returns a string representing the object.
        
        Parameters:
        None

        Returns:
        string: String representing the node object.
        """

        return f'Node at ({self.x},{self.y},{self.z})'

    def to_array(self):
        """
        Returns an array with the object variables.
        
        Parameters:
        None

        Returns:
        numpy array: Array representing the node object.
        """

        return np.array([self.x,self.y,self.z])


class Bar(ElementBase):
    """
    Bar object that represents a line between two nodes and contains stiffness
    and end release information for the element.

    Bar elements may be given a custom name for reference however if no name is
    given the bar will be assigned a guid. Bar names must be unique otherwise 
    bars with confilicting names will be overwritted once added to the database
    model.

    Parameters:
    node_a (node object): Node representing the start point of the bar.
    node_b (node object): Node representing the end point of the bar.
    section (section object): Section property for bar.
    orientation_vector (vector): Vector representing orientation of bar.
    release_a (string): String representing releases of bar start node.
    release_b (string): String representing releases of bar end node.
    name (string): The name of the bar.

    Returns:
    bar objcet: The created bar object.
    """

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self,
                 node_a,
                 node_b,
                 section,
                 orientation_vector,
                 release_a = 'XXXXXX',
                 release_b  = 'XXXXXX',
                 name = None,
                 data = ''
                 ):

        # pylint: disable=too-many-arguments
        # Eight is reasonable in this case.

        self.node_a = node_a
        self.node_b = node_b
        self.section = section
        self.orientation_vector = orientation_vector
        self.release_a = release_a
        self.release_b = release_b
        self.name = name if name is not None else str(uuid.uuid4())
        self.length = 0 #TODO to be implemented
        super().__init__(data)    


class Support(ElementBase):
    """
    Creates a 6 degeree of freedom node support object. Each degree of freedom is represented by a bool.
    True = fixed, False = released.

    Parameters:
    node (node object): The node location of the support.
    fx (bool): The fixity of translations in the x direction.
    fy (bool): The fixity of translations in the y direction.
    fz (bool): The fixity of translations in the z direction.
    mx (bool): The fixity of rotations about the x axis.
    my (bool): The fixity of rotations about the y axis.
    mz (bool): The fixity of rotations about the z axis.

    Returns:
    support object: The defined support object.
    """

    def __init__(self,
                 node,
                 fx,
                 fy,
                 fz,
                 mx,
                 my,
                 mz,
                 data = ''
                 ):

        # pylint: disable=too-many-arguments
        # Seven is reasonable in this case.

        self.node = node
        self.fx = fx
        self.fy = fy
        self.fz = fz
        self.mx = mx
        self.my = my
        self.mz = mz
        super().__init__(data)
    
    def __iter__(self):

        output = [
                  self.fx,
                  self.fy,
                  self.fz,
                  self.mx,
                  self.my,
                  self.mz
                 ]

        return iter(output)

    def __str__(self):

        output_string = []

        for support in list(self):
            if support:
                output_string.append('F')
            else:
                output_string.append('X')
        
        return ''.join(output_string)
        

    def set_fix(self):
        """
        Sets the support to fully fixed.

        Parameters:
        None

        Returns:
        support object: Fully fixed support object.
        """
        self.fx = True
        self.fy = True
        self.fz = True
        self.mx = True
        self.my = True
        self.mz = True

    def set_pin(self):
        """
        Sets the support to pinned with rotoational releases only.

        Parameters:
        None

        Returns:
        support object: Pinned support object.
        """
        self.fx = True
        self.fy = True
        self.fz = True
        self.mx = False
        self.my = False
        self.mz = False
    
    def set_slider(self):
        """
        Sets the support to slider with fz fixed only.

        Parameters:
        None

        Returns:
        support object: Slider support object.
        """
        self.fx = False
        self.fy = False
        self.fz = True
        self.mx = False
        self.my = False
        self.mz = False

    def is_fix(self):

        return all(list(self))
    
    def is_pin(self):
        
        return (all(list(self)[:3]) and not all(list(self)[3::]))
    
    def is_slider(self):

        return (self.fz == True and 
                not all(list(self)[:2]) and 
                not all(list(self)[3::]))

    


    @staticmethod

    def pin(node):
        # pylint: disable=no-self-argument
        """
        Returns a pinned support at the given node location.
        
        Parameters:
        None

        Returns:
        support object: Pinned support object.
        """

        return Support(node,True,True,True,False,False,False)

    def fix(node):
        # pylint: disable=no-self-argument
        """
        Returns a fixed support at the given node location.
        
        Parameters:
        None
        
        Returns:
        support object: Pinned support object.
        """

        return Support(node,True,True,True,True,True,True)
