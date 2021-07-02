#!/bin/env python
#Este módulo crea la base de datos inicial si esta no existe

"""
Tabla settings:
-----
0: False
1: True
-----
actualizar = Configuración relativa a la busqueda de actualizaciones al iniciar el programa
ini_aut = Configura inicio automatico
video = Nombre del video en turno
palabras = Numeros de palabras de búsqueda
scrapers = Lista de nombres de los scrapers utilizados
recode = Opción de recodificar los subtítulos a UTF-8 en caso de poderse
menu = Ultima pantalla accesada
"""

"""
Tabla resultados:
Lista de subtitulos con su respectivo título, descripción y URL de descarga
"""

import sqlite3
import os

def creadb():
    if os.path.isfile("data.db"):
        return "existe"
    else:
        conexion = sqlite3.connect("data.db")
        cursor = conexion.cursor()
        
        cursor.execute("CREATE TABLE resultados (titulo TEXT, descripcion TEXT, url TEXT)")
        cursor.execute("CREATE TABLE settings (actualizar INTEGER, ini_aut INTEGER, ruta_carpeta TEXT, ruta_video TEXT, video TEXT, palabras TEXT, scrapers TEXT, recode INTEGER, menu INTEGER, oneline INTEGER)")

        #valores iniciales
        cursor.execute("INSERT INTO settings VALUES (1, 1, '/home/saul/Python/Android/sub4time/storage/shared/', '', '', '', 'subdivx,opensubtitles', 1, 0, 1)")

        conexion.commit()
        conexion.close()

        return "creado"
