#!/bin/env python

#Lista de los archivos + lista de sus rutas mostrados

from modules.admin_db import read_settings
from subprocess import Popen, PIPE

#Extensions: extensiones separadas por coma
#Route: ruta escaneada
def archivos_en_ruta(extensions:str, route:str):
    extensiones = extensions.split(",")
    archivos = []
    
    clean_route = route.replace("\\'","\'")
    command = ["find", clean_route, "-type", "f", "-iname"]

    for ext in extensiones:
        ext_files = Popen(command + ["*." + ext], stdout=PIPE, stderr=PIPE)
        output, errors = ext_files.communicate()
        archivos += output.decode('utf-8').splitlines()
    archivos = [archivo for archivo in archivos if archivo != ""]
    
    #Lista depurada con los nombres de los archivos
    lista_rutas, lista_archivos = [], []
    for x in archivos:
        if '/' in x:
            index_0 = x.rindex("/")
            index_1 = x.index("/")
            lista_rutas += [x[index_1:index_0 + 1]]
            lista_archivos += [x[index_0 + 1:]]

    return [lista_rutas, lista_archivos]


def subs_en_ruta():
    extensiones = "srt,ssa,ass"
    ruta = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/tmp/"
    return archivos_en_ruta(extensiones, ruta)


def videos_en_ruta():
    extensiones = read_settings("extensions")
    ruta = read_settings("folder_route")

    return archivos_en_ruta(extensiones, ruta)
