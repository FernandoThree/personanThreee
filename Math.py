import math
import numpy
from Math_geo.Point import Point

__RADIUS_PLANET = 6371000.0

"""@function get_distance
    calcuala la distancia entre dos puntos de la tierra
    @param  p1(Point)   punto 1
    @param  p2(Point)   punto 2

    @return (float) distancia entre los puntos
"""
def get_distance( p1: Point, p2: Point) -> float:
    radius_latitud1 = math.radians(p1.latitude)
    radius_latitud2 = math.radians(p2.latitude)
    delta_latitude  = math.radians(p2.latitude  - p1.latitude)
    delta_longitude = math.radians(p2.longitude - p1.longitude)

    a = math.sin(delta_latitude / 2)  * math.sin(delta_latitude / 2) + \
        math.cos(radius_latitud1)    * math.cos(radius_latitud2)   * \
        math.sin(delta_longitude / 2) * math.sin(delta_longitude / 2)
    
    return __RADIUS_PLANET * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

"""@function get_angle
    calcula el angulo formado por dos puntos y un cetro, 
    devuelve el resultado en grados
    @param  center(Point)
    @param  p1(Point)       punto 1
    @param  p2(Point)       punto 2
"""
def get_angle( center: Point, p1: Point, p2: Point) -> float:
    v1 = numpy.array([p1.x - center.x, p1.y - center.y])
    v2 = numpy.array([p2.x - center.x, p2.y - center.y])

    angulo = math.acos(numpy.cross(v1,v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2)))
    return math.degrees(angulo)

"""@function get_decimal_coordinate
    convierte una coordenada a decimal
    @param  coordinate(float)       contiene la coordenada, la parte entera contiene los grados 
                                    y la parte decimal los minutos
    @param  orientation(str(1))     puede ser {N,S,W,E}
    @TODO: revisar si funciona correctamente la conversión con datos reales
"""
def get_decimal_coordinate( coordinate: float, orientation: str):
    minutos, grados = math.modf(coordinate)
    minutos /= 60
    coord = grados + minutos

    if (orientation=='S' or orientation=='W'):
        coord *= -1
    
    return coord

"""@function orientation
    calcula la orientación de un trío ordenado de puntos p, q, r
    @param      p, q, r         trío ordenado de puntos

    @returns    0 : Colinear points 
                1 : Clockwise points 
                2 : Counterclockwise 
"""
def orientation(p, q, r):       
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
    if (val > 0): 
        # Clockwise orientation 
        return 1
    elif (val < 0): 
        # Counterclockwise orientation 
        return 2

    # Colinear orientation 
    return 0

"""@function on_segment
    Given three colinear points p, q, r, the function checks if  
    point q lies on line segment 'pr'  
"""
def on_segment(p, q, r): 
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
        return True
    return False

"""@funtion intersect_lines
    devuelve el punto de intersección entre dos rectas 
"""
def intersect_lines(p11: Point, p12: Point, p21: Point, p22: Point):
    DET_TOLERANCE = 0.00000001

    #línea 1
    dx1 = p12.x - p11.x 
    dy1 = p12.y - p11.y

    #línea 2
    dx2 = p22.x - p21.x 
    dy2 = p22.y - p21.y

    #encontrar intersección
    det = (-dx1 * dy2 + dy1 * dx2)

    if math.fabs(det) < DET_TOLERANCE:
        return (0, 0.0, 0.0) 

    det_inv = 1.0 / det

    r = det_inv * (-dy2 * (p21.x - p11.x) + dx * (p21.y -p11.y))
    s = det_inv * (-dy1 * (p21.x - p11.x) + dx * (p21.y -p11.y))

    xi = (p11.x  + r * dx1 + p21.x  + s * dx2) / 2
    yi = (p11.y + r * dy1 + p21.y + s * yd2) / 2

    return (1, xi, yi)

"""@function intersect_segments
    indica si dos segmentos de recta intersectan 
"""
def intersect_segments(p11: Point, p12: Point, p21: Point, p22: Point):
    EPSILON = 0.00000001

    o1 = orientation(p11, p12, p21) 
    o2 = orientation(p11, p12, p22) 
    o3 = orientation(p21, p22, p11) 
    o4 = orientation(p21, p22, p12) 
  
    # General case 
    if (o1 != o2) and (o3 != o4): 
        return True
  
    # Special Cases 
    if math.fabs(o1) < EPSILON and on_segment(p11, p21, p12): 
        return True
  
    if math.fabs(o2) < EPSILON and on_segment(p11, p22, p12): 
        return True
  
    if math.fabs(o3) < EPSILON and on_segment(p21, p11, p22): 
        return True
  
    if math.fabs(o4) < EPSILON and on_segment(p21, p12, p22): 
        return True
  
    return False