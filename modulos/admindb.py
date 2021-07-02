#!/bin/env python

import sqlite3

#SETTINGS

#Edita en tabla settings
def editar_settings(columna, nuevo_valor):
    conexion = sqlite3.connect('data.db')
    cursor = conexion.cursor()
    cursor.execute("UPDATE settings SET " + columna + "='" + nuevo_valor + "'")
    conexion.commit()
    conexion.close() 

#Lee en tabla settings
#Recibe el nombre de la columna como parámetro y retorna su valor
def leer_settings(columna):
    columnas = ["actualizar", "ini_aut", "ruta_carpeta", "ruta_video","video", "palabras", "scrapers", "recode", "menu", "oneline"]

    conexion = sqlite3.connect('data.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM settings")

    linea_1 = cursor.fetchone()
    conexion.close()

    return linea_1[columnas.index(columna)]


#RESULTADOS

#Edita en tabla resultados, recibe una lista de listas con formato [titulo, descripcion, url]
def editar_resultados(lista_subs):
    conexion = sqlite3.connect('data.db')
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM resultados")
    cursor.executemany("INSERT INTO resultados VALUES (?,?,?)", lista_subs)

    conexion.commit()
    conexion.close()

#Lee en tabla resultados y retorna una lista de tuplas
def leer_resultados():
    conexion = sqlite3.connect('data.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM resultados")

    subs = cursor.fetchall()
    conexion.close()

    return subs
