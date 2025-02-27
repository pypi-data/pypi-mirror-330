"""
This module contains the functions for the geometrical manipulation of vectors.
"""
import math
import numpy as np

class Vector3d(np.ndarray):

    
    def __new__(cls, input_array):
        # Create a new instance of the subclass (Vector), using np.asarray to handle input array
        obj = np.asarray(input_array).view(cls)
        return obj
    

    def __init__(self, input_array):
        if len(input_array) != 3:
            raise ValueError('Input array must contain 3 numbers')
        
        for value in input_array:
            if not (isinstance(value, (int, float, complex)) and not isinstance(value, bool)):
                raise TypeError(['Input array must only contian numbers'])
        
        self._x = input_array[0]
        self._y = input_array[1]
        self._z = input_array[2]
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z
    
    @x.setter
    def x(self, new_value):
        self[0] = new_value
        self._x = new_value
    
    @y.setter
    def y(self, new_value):
        self[1] = new_value
        self._y = new_value
    
    @z.setter
    def z(self, new_value):
        self[2] = new_value
        self._z = new_value

    def magnitude(self):
        return np.linalg.norm(self)

    def unit(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return self / mag

    def dot_product(self, other):
        if isinstance(other, Vector3d):
            return np.dot(self, other)
        else:
            raise ValueError("Dot product requires another Vector3d instance.")
    
    def cross_product(self, other):
        if isinstance(other, Vector3d):
            return np.cross(self, other)
        else:
            raise ValueError("Cross product requires another Vector3d instance.")

    def is_parallel_to(self, other):
        """
        Checks whether two vectors are parallel.

        Parameters:
        other (vector_3d): The second vector to compare.

        Returns:
        bool: 'true' if vectors are parallel and 'false' if
        vectors are not parallel.
        """

        if not isinstance(other, Vector3d):
            raise TypeError('Input must be Vector_3d')
        
        return Vector3d.magnitude(np.cross(self,other)) == 0
    
    def __eq__(self, other):

        if (list(self) == list(other)):
                return True

        return False

                
    @staticmethod
    def unit_x():
        """
        Returns a unit vector oriented to the x-axis
        
        Parameters:
        None

        Returns:
        A unit vector in aligned to the x-axis. 
        """
        return Vector3d([1,0,0])

    @staticmethod
    def unit_y():
        """
        Returns a unit vector oriented to the y-axis
        
        Parameters:
        None

        Returns:
        A unit vector in aligned to the y-axis. 
        """
        return Vector3d([0,1,0])
    
    @staticmethod
    def unit_z():
        """
        Returns a unit vector oriented to the z-axis
        
        Parameters:
        None

        Returns:
        A unit vector in aligned to the z-axis. 
        """
        return Vector3d([0,0,1])

    @staticmethod
    def gram_schmit(vector_1, vector_2):
        """
        Creates an orthogonal vector to the first vector in a plane defined by both vectors.

        Parameters:
        vector_1 (vector_3d): The first vector defining the plane.
        vector_2 (vector_3d): The second vector defining the plane.

        Returns:
        vector (vector_3d): The resultant orthogonal vector.
        """

        if not (isinstance(vector_1, Vector3d) or isinstance(vector_2, Vector3d)):
            raise TypeError('Inputs must be Vector_3d')

        return Vector3d(vector_2 - (np.dot(np.dot(vector_2,vector_1),vector_1)))

    @staticmethod
    def vector_magnitude(vector):

        if not isinstance(vector, Vector3d):
            raise TypeError('Input must be Vector_3d')
        
        return vector.magnitude()

""" Move to point
def length(point_1, point_2):
    
    Gets the length of a vector between two points.
    
    Parameters:
    point_1 (vector_3d): A vector representing a point to
                         calculate length from.
    point_2 (vector_3d): A vector representing a point to
                         calculate length to.

    Returns:
    float: The length of the line.
    
    

    return math.sqrt((point_1[0] - point_2[0])**2
                     + (point_1[1] - point_2[1])**2
                     + (point_1[2] - point_2[2])**2
                     )

"""