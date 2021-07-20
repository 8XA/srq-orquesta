#!/bin/env python

import sqlite3

ruta = "/data/data/com.termux/files/usr/share/sub4time/sub4time/data.db"

#SETTINGS

#Edita en tabla settings
def editar_settings(columna, nuevo_valor):
    global ruta
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("UPDATE settings SET " + columna + "='" + nuevo_valor + "'")
    conexion.commit()
    conexion.close() 

#Lee en tabla settings
#Recibe el nombre de la columna como parámetro y retorna su valor
def leer_settings(columna):
    global ruta
    columnas = ["actualizar", "ini_aut", "ruta_carpeta", "ruta_video","video",
            "palabras", "scrapers", "recode", "menu", "menu_anterior", "oneline", 
            "extensiones", "id_descargable", "cambio_busqueda", "link_descarga",
            "subs_descargados", "rpp", "filtro_videos", "instancia_activa"]

    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM settings")

    linea_1 = cursor.fetchone()
    conexion.close()

    return linea_1[columnas.index(columna)]

#Restaurar backup
def restaurar_settings():
    pass


#RESULTADOS

#Edita en tabla resultados, recibe una lista de listas con formato [titulo, descripcion, url]
def editar_resultados(lista_subs):
    global ruta
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM resultados")
    cursor.executemany("INSERT INTO resultados VALUES (?,?,?)", lista_subs)

    conexion.commit()
    conexion.close()

#Lee en tabla resultados y retorna una lista de tuplas
def leer_resultados():
    global ruta
    conexion = sqlite3.connect(ruta)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM resultados")

    subs = cursor.fetchall()
    conexion.close()

    return subs
