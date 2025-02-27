"""
Contains the object classes for point properties of the structural model.
"""
import numpy as np

class Material:
    """
    Creates a material object from the structural paramaters that define the
    material.

    Parameters:
    name (string): Name of the material.
    youngs_modulus (float): Youngs modulus of the material.
    poissons_ratio (float): Poissons ratio of the material.
    shear_modulus (float): Shear modulus of the material.
    coeff_thermal_expansion (float): Coefficient of thermal expansion of the material.
    damping_ratio (float): Damping ration of the material.
    density (float): Density of the material.
    type (string): Type of the material.
    region (string): Region of the material.
    embodied_carbon (float): Embodied carbon of the material.

    Returns:
    material object: Resulting material object.
    """
    # pylint: disable=too-many-instance-attributes
    # Eleven is reasonable in this case.

    def __init__ (self,
                  name : str,
                  youngs_modulus : float, # MPa
                  poissons_ratio : float,
                  shear_modulus : float, # MPa
                  coeff_thermal_expansion : float, # 1/c
                  damping_ratio : float,
                  density : float, # kN/m^3
                  type : str = None, # pylint: disable=redefined-builtin
                  region: str = None,
                  embodied_carbon : float = None #kgCO2e/m^3
                  ):

        # pylint: disable=too-many-arguments
        # Eleven is reasonable in this case.

        self._id = name
        self.youngs_modulus = youngs_modulus
        self.poissons_ratio = poissons_ratio
        self.shear_modulus = shear_modulus
        self.coeff_thermal_expansion = coeff_thermal_expansion
        self.damping_ratio = damping_ratio
        self.density = density
        self.type = type
        self.region = region
        self.embodied_carbon = embodied_carbon

    @staticmethod

    def default():
        """
        Returns a default steel material if no material is given.
        
        Parameters:
        None

        Returns:
        material object: Material with pre-defined material properties.
        """

        default_material = Material('steel',
                                    210000, # MPa
                                    0.3,
                                    76903.07, # MPa
                                    0.0000117, # 1/c
                                    0,
                                    76.9729, # kN/m^3
                                    'STEEL',
                                    'UK',
                                    12090 #kgCO2e/m^3
                                    )

        return default_material

    def to_string(self):
        """
        Returns a string representing the object.

        Parameters:
        None

        Returns:
        string: String object representing the material.        
        """

        return f'Material: name = {self.name}'

    def to_array(self):
        """
        Returns an array with the object variables.
        
        Parameters:
        None

        Returns:
        numpy array: Array object representing the material.    
        """

        return np.array([self.name,
                         self.youngs_modulus,
                         self.poissons_ratio,
                         self.shear_modulus,
                         self.coeff_thermal_expansion,
                         self.damping_ratio,
                         self.density,
                         self.type,
                         self.region,
                         self.embodied_carbon
                        ]
                        )

class Section:
    """
    Creates a section object from the structural paramaters that define the
    section.

    Parameters:
    name (string): Name of the section.
    material (material object): Material object applied to section.
    area (float): Area of section.
    izz(float): The moment of inertia of the section in the z direction.
    iyy(float): The moment of inertia of the section in the y direction.

    Returns:
    section object: Resultant section object.
    """
    # pylint: disable=too-many-arguments
    # Six is reasonable in this case.

    def __init__ (self,
                  name : str,
                  material : Material,
                  area : float, # sqm
                  izz : float, # m^4
                  iyy : float, # m^4
                  ):

        self._id = name
        self.material = material
        self.area = area
        self.izz = izz
        self.iyy = iyy

    @staticmethod

    def default():
        """
        Returns a default UC305x305x97 section if no section is given.
        
        Parameters: 
        None

        Retruns:
        section object: A section object with default properties.
        """

        default_section = Section('UC305x305x97',
                                  Material.default(),
                                  0.0123, # sqm
                                  0.0002225, # m^4
                                  0.00007308, # m^4
                                  )

        return default_section

    def to_string(self):
        """
        Returns a string representing the object.

        Parameters: 
        None

        Returns:
        string: String object representing the section object.
        """

        return f'Section: name = {self.name}'

    def to_array(self):
        """
        Returns an array with the object variables.
        
        Parameters: 
        None

        Returns:
        numpy array: Array object representing the section object.
        """

        return np.array([self.name,
                         self.material.name,
                         self.area,
                         self.izz,
                         self.iyy]
                         )

class LocalPlane:
    """
    Creates a local plane definig the orienation of a bar object.

    Parameters: 
    origin (numpy array): Origin of the plane.
    x_vector (numpy array): Vector representing orienatation of x-axis of local plane. 
    y_vector (numpy array): Vector representing orienatation of y-axis of local plane. 
    z_vector (numpy array): Vector representing orienatation of z-axis of local plane. 

    Returns:
    local plane object: Resulting local plane object.
    """

    def __init__(self,
                 origin : np.array,
                 x_vector : np.array,
                 y_vector : np.array,
                 z_vector : np.array
                 ):

        self.origin = origin
        self.x_vector = x_vector
        self.y_vector = y_vector
        self.z_vector = z_vector

    def to_string(self):
        """
        Returns a string representing the object.
        
        Parameters: 
        None

        Returns:
        string: String object representing the local plane object.
        """

        return f'Local Plane at {self.origin}'

    def to_array(self):
        """
        Returns an array with the object variables.
        
        Parameters: 
        None

        Returns:
        numpy array: Array object representing the local plane object.
        """

        return np.array([self.origin,
                         self.x_vector,
                         self.y_vector,
                         self.z_vector]
                         )
