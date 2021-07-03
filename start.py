#!/bin/env python

from modulos.creadb import *
creadb()

from modulos.admindb import *
from pantallas.actualizar import *
from pantallas.pelicula import *
from pantallas.carpeta import *
from pantallas.palabras import *
from pantallas.resultados import *
from pantallas.configuracion import *

#Buscar actualizaciones
#if leer_settings("actualizar") == 1:
#    actualizar()

s4t = {
        0: pelicula,
        1: carpeta,
        2: palabras,
        3: resultados,
        4: configuracion,
        #5: ayuda,
        #6: acerca_de,
        }

running = s4t[0]()
while running != 7:
    running = s4t[running]()

