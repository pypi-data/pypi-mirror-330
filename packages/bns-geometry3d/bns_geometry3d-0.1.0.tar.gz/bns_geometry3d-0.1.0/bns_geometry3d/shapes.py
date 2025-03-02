import math

# Constants
PI = math.pi

class BnsGeometry3D:
    """A class to calculate the surface areas of various 3D shapes."""
    
    @staticmethod
    def sphere_area(radius):
        """Calculate the surface area of a sphere."""
        return 4 * PI * radius ** 2

    @staticmethod
    def cylinder_area(radius, height):
        """Calculate the surface area of a cylinder."""
        return 2 * PI * radius * (radius + height)

    @staticmethod
    def cube_area(side):
        """Calculate the surface area of a cube."""
        return 6 * side ** 2
