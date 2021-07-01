#!/bin/env python

import sqlite3

from modulos.creadb import *
from pantallas.pelicula import *
from pantallas.carpeta import *

#Crea base de datos si esta no existe
creadb()

Si buscaractualizaciones =True... pantalla buscar actualizaciones
running = pelicula


while running != "salir":
    if running == "pelicula":
        running = pelicula
    elif running == "carpeta":
        running = carpeta
    
