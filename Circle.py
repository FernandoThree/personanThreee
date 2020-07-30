from Math_geo.Point import Point
from Math_geo.Math import get_distance

"""@class Circle
    define un círuclo con un centro y un radio. Su método principal
    determina si un punto dado está dentro del círculo considierando
    la distancia geográfica.
    @member     __center(Point)     centro del círculo
    @member     __raius(float)      radio del círculo
"""
class Circle:
    """@Constructor
        establece los miembros de la clase
        @param:     center(Point)   centro del círculo
        @param:     radius(float)   radio del círculo
    """
    def __init(self, center: Point = Point(), radius: float = 1000.0):
        self.__center = center
        self.__radius = radius

    """@property center
        propiedad pública para mostrar el miembro __center(Point)
    """
    @property
    def center(self):
        return self.__center
    
    @center.setter
    def center(self, center: Point):
        self.__center = center

    """@property radius
        propiedad pública para mostrar el miembro __radius(float)
    """
    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, radius: float):
        self.__radius = radius

    """@method set
        establece los miembros del Circle
        @param  center(Point)
        @param  radius(float)
    """
    def set(self, center: Point, radius: float):
        self.__center = center
        self.__radius = radius

    """@method distance_to_center
        calcula la distancia de un punto dado al centro del Circle
        @param  point(Point)

        @return (float) distanca del punto al centro
    """
    def distance_to_center( self, point: Point) -> float:
        return get_distance( self, point)

    """@method in_radius
        indica si el punto está dentro del Circle
        @param  point(Point)

        @return (bool) True si dentro del Circle, False si no
    """
    def in_radius(self, point: Point) -> bool:
        return True if distance_to_center(point) <= self.__radius else False

    