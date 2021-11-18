#!/bin/env python

#####################
#leer_settings **
#editar_settings()
#
#editar_resultados
#leer_resultados
#
#restaurar_settings
#
#leer_torrents
#editar_torrents
#####################

import sqlite3, os

ruta = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db"
ruta_backup = "/data/data/com.termux/files/usr/share/srq-orquesta/data_backup.db"

#Lee los datos volátiles y permanentes requeridos por
#las diferentes pantallas

#PARÁMETROS:
#  - 0: True: data | False: data_backup
#  - 1: tabla (settings o datos al vuelo)
#  - 2: columna

#RETORNA:
# - Para data:
#     Retorna valor preciso
      
# - Para data_backup
#     Retorna lista de columnas y valores:
#       [[columna1, columna2],[valor1, valor2]]

def leer_resultados(*args):
    global ruta, ruta_backup

    data, columna = ruta_backup, '*'
    if args[0] == True:
        data = ruta
        columna = args[2]

    conexion = sqlite3.connect(data)
    cursor = conexion.cursor()
    cursor.execute("SELECT " + columna + " FROM " + args[1])

    columnas_backup = [descripcion[0] for descripcion in cursor.description]

    #Lectura de primera línea
    valores = cursor.fetchone()
    conexion.close()

    if columna == '*':
        return [columnas_backup, valores]
    return valores[0]
    

#Edita un valor individual de las tablas de datos volátiles y permanentes
def editar_resultados(tabla, columna, nuevo_valor):
    global ruta

    if os.path.isfile(ruta):
        conexion = sqlite3.connect(ruta)
        cursor = conexion.cursor()
        cursor.execute("UPDATE " + tabla + " SET " + columna + "='" + nuevo_valor + "'")
        conexion.commit()
        conexion.close() 

#leer_resultados(torrents o subs)
#editar_resultados(torrents o subs)
#  -- Agregar lista
#  -- Vaciar lista
#  -- Editar estado
#
#leer_datos(settings o al vuelo)
#editar_datos(settings o al vuelo)
#  -- Modificar valor específico
#
#leer_lista_simple
#editar_lista_simple
#  -- Agregar elemento a la lista
#  -- Eliminar elemento de la lista
#  -- Limpiar tabla
#
#RESTAURAR
#
