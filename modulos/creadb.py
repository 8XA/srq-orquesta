#!/bin/env python
#Este módulo crea la base de datos inicial si esta no existe

#Tabla settings:
#-----
#0: False
#1: True
#-----

#actualizar = Configuración relativa a la busqueda de 
#actualizaciones al iniciar el programa

#ini_aut = Configura inicio automatico
#ruta_carpeta = ruta de la carpeta de los videos mostrados
#ruta_video = ruta de la carpeta del video seleccionado
#video = Nombre del video en turno
#palabras = Numeros de palabras de búsqueda
#scrapers = Lista de nombres de los scrapers utilizados
#recode = Opción de recodificar los subtítulos a UTF-8 en caso de poderse
#menu = Ultima pantalla accesada
#menu_anterior = Pantalla anterior a la actual
#oneline = Si esta activo, muestra los videos y carpetas en una sola linea
#extensiones_activas = extensiones de video activas
#extensiones_disponibles = extensiones de video disponibles
#cambio_busqueda = True si los parametros de busqueda (video, ruta o palabras) cambiaron
#
#Tabla resultados:
#Lista de subtitulos con su respectivo título, descripción y URL de descarga

import sqlite3
import os

def creadb():
    ruta = "/data/data/com.termux/files/usr/share/sub4time/sub4time/data.db"

    if os.path.isfile(ruta):
        return "existe"
    else:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
        
        cursor.execute("CREATE TABLE resultados (titulo TEXT, descripcion TEXT, url TEXT)")
        cursor.execute("CREATE TABLE settings (actualizar INTEGER, ini_aut INTEGER, \
                ruta_carpeta TEXT, ruta_video TEXT, video TEXT, palabras TEXT, scrapers TEXT, \
                recode INTEGER, menu INTEGER, menu_anterior INTEGER, oneline INTEGER, \
                extensiones TEXT, id_descargable TEXT, cambio_busqueda INTEGER, \
                link_descarga TEXT, subs_descargados TEXT, rpp int, filtro_videos TEXT, \
                filtro_resultados TEXT, instancia_activa INTEGER)")

        #valores iniciales
        cursor.execute("INSERT INTO settings VALUES (1, 1, '/sdcard/', '', '', '', \
                'subdivx', 0, 0, 0, 1, 'mkv,avi,mp4', 'disponibles', 0, '', '', 50, \
                '', '', 0)")

        conexion.commit()
        conexion.close()

        return "creado"
