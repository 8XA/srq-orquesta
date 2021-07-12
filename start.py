#!/bin/env python

from modulos.creadb import *
creadb()

import readline
from modulos.admindb import leer_settings
from pantallas.actualizar import *
from pantallas.pelicula import *
from pantallas.carpeta import *
from pantallas.palabras import *
from pantallas.resultados import *
from pantallas.configuracion import *
from pantallas.ayuda import *
from pantallas.acerca_de import *
from pantallas.descarga import *

s4t = {
        0: pelicula,
        1: carpeta,
        2: palabras,
        3: resultados,
        4: configuracion,
        5: ayuda,
        6: acerca_de,
        101: descarga,
        102: actualizar,
        }

#Loop verificador de acceso a /sdcard


#Buscar actualizaciones
if leer_settings("actualizar") == 1:
    actualizar()

running = s4t[0]()
while running != 100:
    running = s4t[running]()

