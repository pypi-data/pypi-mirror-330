"""
This module contains the functions for the geometrical manipulation of planes.
"""

import numpy as np
from . import vector3d # pylint: disable=import-error

def plane_from_3pt(point_1, point_2, oreintation_vector, x_axis_oriented = True):
    """
    This function builds a plane from:

     -An orientation vector defining the orinetation of the x axis

     If the orientation vector defines the orientation of the y-axis 
     set the x_axis_oriented boolean to false.

    Parameters:
    point_1 (vector_3d):A point defining the start of a line.
    point_2 (vector_3d):A point defining the end of a line.
    oreintation_vector (vector_3d): an orientation vector defining the 
                                    orientation of the plane.
    x_axis_oriented (bool): a boolean specifying which axis is aligned
                            with the orientation vector. If 'true' then
                            x-axis is aligned, if 'false' then y-axis 
                            is aligned.

    Returns:
    origin (vector_3d): A vector defining the origin of the plane.
    x_vector (vector_3d): A vector defining the x-axis of the plane.
    y_vector (vector_3d): A vector defining the y-axis of the plane.
    z_vector (vector_3d): A vector defining the z-axis of the plane.
    """

    origin = point_1
    x_vector = vector3d.unit(point_2 - point_1)
    

    if vector3d.is_parallel(x_vector , oreintation_vector):
        if not vector3d.is_parallel(x_vector , vector3d.unit_z()):
            oreintation_vector = vector3d.unit_z()
        else:
            oreintation_vector = -vector3d.unit_x()


    y_vector = vector3d.unit(vector3d.gram_schmit(x_vector, oreintation_vector))
    z_vector = vector3d.unit(np.cross(x_vector, y_vector))


    if not x_axis_oriented:
        x_vector , y_vector , z_vector = y_vector , z_vector, x_vector

    return origin , x_vector , y_vector , z_vector
