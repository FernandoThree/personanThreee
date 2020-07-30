from typing import NamedTuple, List
from Almacenamiento.Tablas import Viaje, Viaje_Posicion, Viaje_Trecho

class Posicion_Viaje(NamedTuple):
    posicion      : Viaje_Posicion
    viaje         : Viaje
    viaje_trechos : List[Viaje_Trecho]
    resultado     : dict
