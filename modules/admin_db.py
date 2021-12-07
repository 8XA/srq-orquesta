#!/bin/env python

#This module has the functions to read and edit the database and its backup

from sqlite3 import connect
from os.path import isfile

data_route = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db"
data_backup_route = "/data/data/com.termux/files/usr/share/srq-orquesta/data_backup.db"

######################################################################

def settings_read(
        column:str='*',
        db:str='data_route'
    ):

    """TABLE:
        - settings

    PARAMETERS:
        - column: The column that contains the wished value.
        - db: The database route you are working with, this is 'data_route' by
            default and it can be 'data_backup_route'

    HOW TO USE:
        - Get a value:
            call settings_read('column_name')
        - Get the backup values list:
            call settings_read(db='data_backup_route')

    RETURNS:
        - If you specify a column name:
            It returns that particular value.
         
        - If you don't specify a column name:
            It return all the settings values with this format:
                [[column1, column2], [value1, value2]]
    """

    global data_route, data_backup_route

    db_keys = {
            'data_route': data_route,
            'data_backup_route': data_backup_route
            }

    connection = connect(db_keys[db])
    cursor = connection.cursor()
    cursor.execute("SELECT " + column + " FROM settings")

    #Gets a list of all the column names
    column_names = [column_name[0] for column_name in cursor.description]

    #Reads the first row
    values = cursor.fetchone()
    connection.close()

    if column == '*':
        return [column_names, values]
    return values[0]
    

##Edita un valor individual de las tablas de datos volátiles y permanentes
#def editar_resultados(tabla, columna, nuevo_valor):
#    global ruta
#
#    if os.path.isfile(ruta):
#        conexion = sqlite3.connect(ruta)
#        cursor = conexion.cursor()
#        cursor.execute("UPDATE " + tabla + " SET " + \
#                columna + "='" + str(nuevo_valor) + "'")
#        conexion.commit()
#        conexion.close() 
#
#######################################################################
#
##TABLAS:
##    -- torrents (lista de torrents hallados)
##    -- subtitulos (lista de subtítulos hallados)
#
##PARÁMETROS
##  - 0: True: data | False: data_backup
##  - 1: tabla (torrents o subtitulos)
#
##RETORNA:
## - Lista con resultados:
#      
#def leer_resultados(*args):
#    global ruta, ruta_backup
#
#    data = ruta_backup
#    columna = '*'
#    if args[0] == True:
#        data = ruta
#        columna = args[2]
#
#    conexion = sqlite3.connect(data)
#    cursor = conexion.cursor()
#    cursor.execute("SELECT " + columna + " FROM " + args[1])
#
#    columnas_backup = [descripcion[0] for descripcion in cursor.description]
#
#    #Lectura de primera línea
#    valores = cursor.fetchone()
#    conexion.close()
#
#    if columna == '*':
#        return [columnas_backup, valores]
#    return valores[0]
#    
#
##Edita un valor individual de las tablas de datos volátiles y permanentes
#def editar_resultados(tabla, columna, nuevo_valor):
#    global ruta
#
#    if os.path.isfile(ruta):
#        conexion = sqlite3.connect(ruta)
#        cursor = conexion.cursor()
#        cursor.execute("UPDATE " + tabla + " SET " + \
#                columna + "='" + str(nuevo_valor) + "'")
#        conexion.commit()
#        conexion.close() 
#
#######################################################################
#
#def leer_resultados(booleano, tabla):
#    global ruta, ruta_backup
#    
#    data = ruta_backup
#    if args[0] == True:
#        data = ruta
#    
#    conexion = sqlite3.connect(data)
#    cursor = conexion.cursor()
#    cursor.execute("SELECT * FROM " + tabla)
#
#    resultados = cursor.fetchall()
#    conexion.close()
#
#    return resultados
#
##PARÁMETROS:
##  - 0: modo (limpia: limpia lista | reemplaza: reemplaza lista |
##           modifica: actualiza status de elemento)
##  - 1: tabla (torrents o subtitulos)
##  - 2: reemplazo (nueva lista o nuevo status, según el caso)
##  - 3: num_id (Número id a modificar)
#
#def editar_resultados(*args):
#    modo = args[0]
#    tabla = args[1]
#    reemplazo = args[2]
#    num_id = args[3]
#
#    global ruta
#
#    signos = "?,?,?,?"
#    if tabla == "torrents":
#        signos = "?,?,?,?,?,?"
#
#    conexion = sqlite3.connect(ruta)
#    cursor = conexion.cursor()
#
#    if modo == "modifica":
#        cursor.execute("UPDATE " + tabla + " SET status = '" + \
#                str(reemplazo) + "' WHERE rowid = " + str(num_id + 1))
#
#    else:
#        cursor.execute("DELETE FROM " + tabla)
#        if modo == "reemplaza":
#            cursor.executemany("INSERT INTO " + tabla + " VALUES (" + signos + ")", reemplazo)
#
#    conexion.commit()
#    conexion.close()
#
#######################################################################
#
##leer_lista_simple
##editar_lista_simple
##  -- Agregar elemento a la lista
##  -- Eliminar elemento de la lista
##  -- Limpiar tabla
##
##RESTAURAR
##
