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

while running != "salir":
    if running == "pelicula":
        running = pelicula()
    elif running == "carpeta":
        running = carpeta()
    elif running == "palabras":
        running = palabras()
    elif running == "resultados":
        running = resultados()
    elif running == "configuracion":
        running = configuracion()
    elif running == "ayuda":
        running = ayuda()
    elif running == "acerca_de":
        running = acerca_de()
