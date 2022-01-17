#!/bin/env python

#Lista de los archivos + lista de sus rutas mostrados

from modules.admin_db import read_settings
from subprocess import Popen, PIPE
import os

#Extensions: extensiones separadas por coma
#Route: ruta escaneada
def archivos_en_ruta(extensions:str, route:str):
    extensiones = extensions.split(",")
    archivos = []

    for ext in extensiones:
        ext_files = Popen("find '" + route + "' -iname '*." + ext + "'", \
                shell=True, stdout=PIPE, stderr=PIPE)
        archivos += str(ext_files.stdout.read()).split("\\n")
    archivos = [archivo for archivo in archivos if archivo != ""]
    
    #Lista depurada con los nombres de los archivos
    lista_rutas, lista_archivos = [], []
    for x in archivos:
        if '/' in x:
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
