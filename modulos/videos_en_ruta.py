#!/bin/env python

#Lista de videos existentes en la ruta especificada

from modulos.admindb import leer_settings
import os

def videos_en_ruta():
    extensiones = leer_settings("extensiones_activas").split(",")
    videos = []

    for ext in extensiones:
        videos += os.popen("find '" + leer_settings("ruta_carpeta") + "' -iname *." + ext).read().split("\n")
    videos = [video for video in videos if video != ""]
    
    #Lista depurada con los nombres de los videos
    nombres_puros = [ruta[len(ruta) - [ruta[x] for x in range(len(ruta)-1,-1,-1)].index("/"):] for ruta in videos]
    
    return nombres_puros
