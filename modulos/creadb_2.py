#!/bin/env python

#Este módulo crea la base de datos inicial si esta no existe

#Valores booleanos:
#-----
#0: False
#1: True
#-----

import sqlite3
import os

def creadb():
    ruta = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db"

    if os.path.isfile(ruta):
        return "existe"
    else:
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()

        #TABLAS
        ##################################################
        
        #Tabla Torrents
        cursor.execute("CREATE TABLE torrents ("\
                #Nombre del torrent
                "titulo TEXT, " + \
                #Número de sembradores del torrent
                "seeds INTEGER, " +\
                #Número de sanguijuelas
                "leechers INTEGER, " +\
                #Plataforma de donde se obtuvo el torrent
                "procedencia TEXT, " +\
                #Enlace magnético
                "magnetlink TEXT, " +\
                #Estado:
                    #0: No descargado
                    #1: Descargado
                    #2: Último descargado (actual)
                "status INTEGER " +\
                ")")

        ##################################################

        #Tabla Resultados (lista de subtítulos)
        cursor.execute("CREATE TABLE resultados ("\
                #Nombre del subtítulo
                "titulo TEXT, " + \
                #Descripción del subtítulo
                "descripcion TEXT, " + \
                #URL del subtítulo
                "url TEXT, " + \
                #Estado:
                    #0: No descargado
                    #1: Descargado
                    #2: Último descargado (actual)
                "status INTEGER " +\
                ")")

        ##################################################

        #Tabla settings
        cursor.execute("CREATE TABLE settings ("\
                #Actualizar automáticamente al iniciar
                "auto_update INTEGER, " +\
                #Iniciar al abrir Termux
                "auto_inicio INTEGER, " +\
                #Scrapers de subtítulos
                "scrapers_sub TEXT, " + \
                #Scrapers de torrents
                "scrapers_torr TEXT, " + \
                #Recodificar subtítulos a UTF-8
                "recodificar INTEGER, " +\
                #Un renglón por elemento en listas
                "una_linea INTEGER, " +\
                #Extensiones de video admitidas en sección 'Videos'
                "extensiones TEXT, " + \
                #IDs descargables (Torrents y subtítulos)
                "IDs_descargables TEXT, " + \
                #Resultados por página (Torrents y subtítulos)
                "rpp INTEGER " +\
                ")")

        #Valores iniciales de settings
        cursor.execute("INSERT INTO settings (auto_update) VALUES (1)")
        cursor.execute("UPDATE settings SET auto_inicio = 1")
        cursor.execute("UPDATE settings SET scrapers_sub = 'subdivx'")
        cursor.execute("UPDATE settings SET scrapers_torr = 'tpb,yts,rarbg'")
        cursor.execute("UPDATE settings SET recodificar = 0")
        cursor.execute("UPDATE settings SET una_linea = 1")
        cursor.execute("UPDATE settings SET extensiones = 'avi,mp4,mkv'")
        cursor.execute("UPDATE settings SET IDs_descargables = 'disponibles'")
        cursor.execute("UPDATE settings SET rpp = 50")

        ##################################################

        #Tabla datos al vuelo
        cursor.execute("CREATE TABLE datos_al_vuelo ("\
                #Indica si hay una instancia SRQ ORQUESTA en ejecución al iniciar
                "instancia_activa INTEGER, " +\
                #Enlace de descarga del subtítulo seleccionado, 
                #para su respectiva pantalla
                "link_descarga_sub TEXT, " +\
                #Ruta de carpeta de búsqueda de videos
                "ruta_carpeta TEXT, " +\
                #Nombre del video seleccionado
                "video TEXT, " +\
                #Número del menú actual
                "menu INTEGER, " +\
                #Número del menú anterior
                "menu_anterior INTEGER, " +\
                #Indica si la búsqueda de subtítulos cambió
                "cambio_busqueda_subs INTEGER, " +\
                #Indica si la búsqueda de torrents cambió
                "cambio_busqueda_torr INTEGER, " +\
                #Palabras de búsqueda de subtítulos
                "palabras_sub TEXT, " +\
                #Palabras de búsqueda de torrents
                "palabras_torr TEXT, " +\
                #Filtro de sección 'Torrents'
                "filtro_torrents TEXT, " +\
                #Filtro de sección 'Videos'
                "filtro_videos TEXT, " +\
                #Filtro de sección 'Resultados'
                "filtro_resultados TEXT " +\
                ")")

        #Valores iniciales de datos al vuelo
        cursor.execute("INSERT INTO datos_al_vuelo (instancia_activa) VALUES (0)")
        cursor.execute("UPDATE datos_al_vuelo SET link_descarga_sub = ''")
        cursor.execute("UPDATE datos_al_vuelo SET ruta_carpeta = '/sdcard/'")
        cursor.execute("UPDATE datos_al_vuelo SET video = ''")
        cursor.execute("UPDATE datos_al_vuelo SET menu = 0")
        cursor.execute("UPDATE datos_al_vuelo SET menu_anterior = 0")
        cursor.execute("UPDATE datos_al_vuelo SET cambio_busqueda_subs = 0")
        cursor.execute("UPDATE datos_al_vuelo SET cambio_busqueda_torr = 0")
        cursor.execute("UPDATE datos_al_vuelo SET palabras_sub = ''")
        cursor.execute("UPDATE datos_al_vuelo SET palabras_torr = ''")
        cursor.execute("UPDATE datos_al_vuelo SET filtro_torrents = ''")
        cursor.execute("UPDATE datos_al_vuelo SET filtro_videos = ''")
        cursor.execute("UPDATE datos_al_vuelo SET filtro_resultados = ''")

        ##################################################

        #Lista de videos reproducidos
        #Marca el contenido de esta lista en la sección 'Videos'
        cursor.execute("CREATE TABLE reproducidos ("\
                #Video reproducido con ruta
                "video TEXT " +\
                ")")

        ##################################################

        #Lista subtítulos descargados
        #Auxiliar al eliminar carpetas de torrent vacías
        cursor.execute("CREATE TABLE subs ("\
                #Subtítulo descargado con ruta
                "sub TEXT " +\
                ")")

        ##################################################

        conexion.commit()
        conexion.close()

        return "creado"

