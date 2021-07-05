#!/bin/env python

#Lista de los videos + lista de sus rutas mostrados
#A partir de la carpeta actual

from modulos.admindb import leer_settings
import os

#Determina el indice del ultimo slash en un string
def indice(ruta):
    ruta.rindex("/")

def videos_en_ruta():
    extensiones = leer_settings("extensiones_activas").split(",")
    videos = []

    for ext in extensiones:
        videos += os.popen("find '" + leer_settings("ruta_carpeta") + \
                "' -iname *." + ext).read().split("\n")
    videos = [video for video in videos if video != ""]
    
    #Lista depurada con los nombres de los videos
    lista_rutas, lista_videos = [], []
    for x in videos:
        indice = x.rindex("/")
        lista_rutas += [x[:indice + 1]]
        lista_videos += [x[indice + 1:]]

    return [lista_rutas, lista_videos]
