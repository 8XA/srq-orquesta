#!/bin/env python

#import sqlite3

from modulos.creadb import *
creadb()

from modulos.admindb import *
from pantallas.pelicula import *
from pantallas.carpeta import *
from pantallas.actualizar import *

#Buscar actualizaciones
#if leer_settings("actualizar") == 1:
#    actualizar()

running = pelicula()

pantallas = ["pelicula","carpeta","palabras","resultados","configuracion","ayuda","acerca_de", "salir"]

while running != 7:
    if running == 0:
        running = pelicula()
    elif running == 1:
        running = carpeta()
    elif running == 2:
        running = palabras()
    elif running == 3:
        running = resultados()
    elif running == 4:
        running = configuracion()
    elif running == 5:
        running = ayuda()
    elif running == 6:
        running = acerca_de()
