from typing import NamedTuple

"""@class Poit(NamedTuple)
    define un punto geográfico
    @member     latitude(float)
    @member     longitude(float)
"""
class Point(NamedTuple):
    latitude:  float = 0.0
    longitude: float = 0.0

    @property
    def x(self):
        return self.latitude

    @x.setter
    def x(self, x):
        self.latitude = x

    @property
    def y(self):
        return self.longitude

    @y.setter
    def y(self, y):
        self.longitude = y