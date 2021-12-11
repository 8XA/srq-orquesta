#!/bin/env python

from modules.create_db import create_db
create_db()
from modules.admin_db import read_settings, edit_settings, restore_settings
restore_settings()

import readline
from os import system
from screens.update import update
from screens.torrents import *
from screens.pelicula import *
from screens.carpeta import *
from screens.palabras import *
from screens.resultados import *
from screens.configuracion import *
from screens.ayuda import *
from screens.acerca_de import *
from screens.descarga import *
from screens.unasesion import una_sesion
from modules.storage_verify import *
from modules.columns_number import columns_number_func

columns_num = columns_number_func()

#Si ocurre un problema, reinicia la base de datos
#try:
#El programa inicia sólo si no se está
#ejecutando otra instancia
if read_settings("active_instance") == 0:
    edit_settings("active_instance", "1")

    s4t = {
            0: torrents,
            1: pelicula,
            2: carpeta,
            3: palabras,
            4: resultados,
            5: configuracion,
            6: ayuda,
            7: acerca_de,
            101: descarga,
            102: update,
            }

    #Loop verificador de acceso a /sdcard
    storage_verify()

    #Buscar actualizaciones
    ejecutar = 1
    if read_settings("auto_update") == 1:
        ejecutar = update()

    if ejecutar != 100:
        running = s4t[1]()
        while running != 100:
            running = s4t[running]()
    edit_settings("active_instance", "0") 

else:
    una_sesion()

#except Exception as e:
#    print(e)
#    print()
#
#    system("rm '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db'")
#    print(fit_frase(columns_num, "Base de datos corrupta fue corregida. Reinicia Termux..."))
#    input()
