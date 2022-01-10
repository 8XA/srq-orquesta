#!/bin/env python

#Lista de los archivos + lista de sus rutas mostrados

from modules.admin_db import read_settings
import os

#args[0]: extensiones separadas por coma
#args[1]: ruta escaneada
def archivos_en_ruta(*args):
    extensiones = args[0].split(",")
    archivos = []

    for ext in extensiones:
        archivos += os.popen("find '" + args[1] + \
                "' -iname '*." + ext + "'").read().split("\n")
    archivos = [archivo for archivo in archivos if archivo != ""]
    
    #Lista depurada con los nombres de los archivos
    lista_rutas, lista_archivos = [], []
    for x in archivos:
        indice = x.rindex("/")
        lista_rutas += [x[:indice + 1]]
        lista_archivos += [x[indice + 1:]]

    return [lista_rutas, lista_archivos]


def subs_en_ruta():
    extensiones = "srt,ssa,ass"
    ruta = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/tmp/"
    return archivos_en_ruta(extensiones, ruta)


def videos_en_ruta():
    extensiones = read_settings("extensions")
    ruta = read_settings("folder_route")
    return archivos_en_ruta(extensiones, ruta)
