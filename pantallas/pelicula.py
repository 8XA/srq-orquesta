#!/bin/env python

from termcolor import colored
from modulos.numcols import *
from modulos.archivos_en_ruta import videos_en_ruta
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu
from modulos.fit_frases import fit_frase
import os

def pelicula():
    numcols = num_cols()
    titulo = "SUB4TIME v1.0.0"

    rutas_y_videos = videos_en_ruta()
    videos = rutas_y_videos[1]
    rutas = rutas_y_videos[0]
    
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","0")

    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])


    marca_en_pantalla = False
    indice_marcado = -1

    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo)
    print(linea_azul)

    print(((numcols-14)//2)*" " + "Elige un video")

    #IMPRIME NOMBRES DE VIDEOS
    for x in range(len(videos)):
        print(numcols * "-")

        #Marca el video seleccionado actual
        if (leer_settings("ruta_video") != "") and \
           (leer_settings("ruta_video") == rutas[x]) and \
           (leer_settings("video") == videos[x]):

            marca_en_pantalla, indice_marcado = True, x
            indice = colored(str(x), 'green', 'on_white', attrs=['bold', 'dark'])
        else:
            indice = colored(str(x), 'green', attrs=['bold', 'dark'])

        imprimir = indice + ": " + videos[x]
        if leer_settings("oneline") == 1:
            imprimir = imprimir[:numcols + len(indice) - len(str(x))]
        print(imprimir)
    if len(videos) == 0:
        msj = "Nada para mostrar. Prueba con otra carpeta..."
        print(numcols * "-")
        print("\n")
        print(fit_frase(numcols, msj))
        print("\n")

    print(linea_azul)
    print(linea_roja)
    print(leer_settings("ruta_carpeta"))
    print(linea_roja)

    i = menu(numcols)

    if type(i[1]) is str:
        valor_numerico = ((len([x for x in i[1] if x in "0123456789"]) == len(i[1])) and (i[1] != ""))

    if i[0] == "menu":
        return i[1]
    elif (marca_en_pantalla) and ((i[1] == "") or \
            (valor_numerico and (int(i[1]) == indice_marcado))):
        return 2
    else:
        #Registrar opción
        if (
            #Es valor numérico
            valor_numerico and \

            #Esta dentro del rango de opciones
            (int(i[1]) < len(videos)) and \

            #Sentencias or
            #Rutas de video seleccionado y del ya registrado difieren
            ((leer_settings("ruta_video") != rutas[int(i[1])]) or \
            
            #Cambió el nombre del video
            (leer_settings("video") != videos[int(i[1])]))
            ):

            editar_settings("cambio_busqueda", "1")
            editar_settings("video", videos[int(i[1])])
            editar_settings("subs_descargados", "")
            editar_settings("palabras", "")
            editar_settings("ruta_video", rutas[int(i[1])])
            return 2

        return 0

