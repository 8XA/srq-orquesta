#!/bin/env python

import sqlite3, os

ruta = "/data/data/com.termux/files/usr/share/sub4time/sub4time/data.db"
ruta_backup = "/data/data/com.termux/files/usr/share/sub4time/data_backup.db"

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
#Con 'backup' como segundo parámetro, retorna la lectura del backup
def leer_settings(*args):
    global ruta, ruta_backup
    columna = args[0]
    
    columnas = ["actualizar", "ini_aut", "ruta_carpeta", "ruta_video","video",
            "palabras", "scrapers", "recode", "menu", "menu_anterior", "oneline", 
            "extensiones", "id_descargable", "cambio_busqueda", "link_descarga",
            "subs_descargados", "rpp", "filtro_videos", "filtro_resultados",
            "instancia_activa"]

    data = ruta
    if (len(args) > 1) and (args[1] == "backup"):
        data = ruta_backup

    conexion = sqlite3.connect(data)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM settings")

    if (len(args) > 1) and (args[1] == "backup"):
        columnas_backup = [descripcion[0] for descripcion in cursor.description]

    linea_1 = cursor.fetchone()
    conexion.close()

    #Si es lectura de backup, retorna tupla con lista de columnas,
    #y tupla de valores
    if (len(args)) > 1 and (args[1] == "backup"):
        return columnas_backup, linea_1
    return linea_1[columnas.index(columna)]


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
def leer_resultados(*args):
    global ruta, ruta_backup
    
    data = ruta
    if (len(args) == 1) and (args[0] == "backup"):
        data = ruta_backup

    conexion = sqlite3.connect(data)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM resultados")

    subs = cursor.fetchall()
    conexion.close()

    return subs


#RESTAURAR BACKUP
def restaurar_settings():
    global ruta_backup 

    if os.path.isfile(ruta_backup):
        settings = leer_settings("","backup")

        for x in range(len(settings[0])):
            editar_settings(settings[0][x], str(settings[1][x]))
        editar_settings("instancia_activa", "0")
        
        subs = leer_resultados("backup")
        editar_resultados(subs)
    
    os.system("rm " + ruta_backup)

