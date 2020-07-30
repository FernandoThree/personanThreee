from typing import List
from Math_geo.Point import Point
import Math_geo.Math as Math
import sys

"""@class Polygon
    define un póligono con una lista de vértices
    @member     __vertices(List[Point])         lista de vértices
"""
class Polygon:
    #Constant
    __MARGEN_ERROR = 2.0

    """@Constructor
        establece los miembros de la clase
        @param:     vertices(List[Point])       lista de vértices
    """
    def __init__(self, vertices: List[Point] = []):
        self.__vertices = vertices

    """@property vertices
        propiedad pública para mostar el miembro __vertices(List[Point])
        @param      vertices(List[Point])       lista de vértices
    """
    @property
    def vertices(self):
        return self.__vertices

    @property
    def aristas(self):
        aristas = []
        for i in range(len(self.vertices) - 1):
            arista = (self.vertices[i], self.vertices[i+1])
            aristas.append(arista)
        aristas.append((self.vertices[-1], self.vertices[0]))

        return aristas

    @vertices.setter
    def vertices(self, vertices):
        self.__vertices = vertices

    """@method append
        agrega un punto al final de la lista de vértices
        @param  punto(Point)
    """
    def append(self, punto: Point):
        self.__vertices.append(punto)

    """@method insert
        agrega un punto en el indice indicado
        @param  index(int)
        @param  point(Punto)
    """
    def insert(self, index: int , point: Point):
        self.__vertices.insert(index, point)

    """@method in_polygon_angle
        calcula la suma de los ángulos formados por los vértices del polígino
        y un punto indicado, se utiliza para verificar si un punto está dentro
        del polígono
        @param      point(Point)

        @return     (float)         devuelve la suma de los ángulos
    """
    def in_polygon_angle(self, punto: Point) -> float:
        #se valida que el Polygon tenga al menos 3 vértices
        if (len(self.__vertices) < 3):
            return -1

        angulo   = 0.0
        puntoAnt = self.__vertices[0]

        for p in self.__vertices[1:]:
            angulo += abs(Math.get_angle(punto, puntoAnt, p))
            puntoAnt = p
        
        angulo += abs(Math.get_angle(punto, puntoAnt, self.__vertices[0]))

        return angulo

    def in_polygon(self, punto: Point) -> bool:
        # return True if self.in_polygon_angle(punto) >= 360 - self.__MARGEN_ERROR else False
        cuenta  = 0
        for arista in self.aristas:
            if Polygon.ray_intersect(punto, *arista):
                cuenta +=1
        
        #inpar
        if (cuenta % 2) == 1:
            return True
        
        return False

    """@staticmethod ray_intersect      @TODO: ver si mover a librería Math
        algoritmo ray casting para determinar si un punto está dentro de un polígono
    """
    @staticmethod
    def ray_intersect(punto: Point, p1: Point, p2: Point) -> bool:
        EPSILON = 0.0001
        
        p_min = None
        p_max = None
        if p1.y < p2.y:
            p_min = p1
            p_max = p2
        else:
            p_min = p2
            p_max = p1

        if punto.y == p_min.y or punto.y == p_max.y:
            punto.y += EPSILON
        
        if punto.y < p_min.y or punto.y > p_max.y:
            return False
        elif punto.x >= max(p_min.x, p_max.x):
            return False
        else:
            if punto.x < min(p_min.x, p_max.x):
                return True
            else:
                if p_min.x != p_max.x:
                    m_red = (p_max.y - p_min.y)/(p_max.x - p_min.x)
                else:
                    m_red = sys.maxsize

                if p_min.x != punto.x:
                    m_blue = (punto.y - p_min.y)/(punto.x - p_min.x)
                else:
                    m_blue = sys.maxsize

                if m_blue >= m_red:
                    return True
                else:
                    return False

