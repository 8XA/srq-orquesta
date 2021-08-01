#!/bin/env python

from modulos.creadb import *
creadb()
from modulos.admindb import leer_settings, restaurar_settings
restaurar_settings()

import readline, os
from pantallas.actualizar import *
from pantallas.pelicula import *
from pantallas.carpeta import *
from pantallas.palabras import *
from pantallas.resultados import *
from pantallas.configuracion import *
from pantallas.ayuda import *
from pantallas.acerca_de import *
from pantallas.descarga import *
from pantallas.unasesion import una_sesion
from modulos.storage_verify import *
from modulos.numcols import num_cols

numcols = num_cols()

#Si ocurre un problema, reinicia la base de datos
try:
    #El programa inicia sólo si no se está
    #ejecutando otra instancia
    if leer_settings("instancia_activa") == 0:
        editar_settings("instancia_activa", "1")

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
        storage_verify()

        #Buscar actualizaciones
        ejecutar = 1
        if leer_settings("actualizar") == 1:
            ejecutar = actualizar()

        if ejecutar != 100:
            running = s4t[0]()
            while running != 100:
                running = s4t[running]()
        editar_settings("instancia_activa", "0") 

    else:
        una_sesion()

except Exception as e:
    print(e)
    print()

    os.system("rm '/data/data/com.termux/files/usr/share/apocalipsis-orquesta/apocalipsis-orquesta/data.db'")
    print(fit_frase(numcols, "Base de datos corrupta fue corregida. Reinicia Termux..."))
    input()
