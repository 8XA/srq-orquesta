#!/bin/env python

from termcolor import colored
from modulos.numcols import *
from modulos.videos_en_ruta import *
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu
import os

numcols = num_cols()
version = "SUB4TIME v1.0.0"
videos = videos_en_ruta()
editar_settings("menu","0")

def pelicula():
    os.system("clear")

    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))
    print(((numcols-len(version))//2) * " " + version)
    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))
    print(((numcols-14)//2)*" " + "Elige un video")

    #IMPRIME NOMBRES DE VIDEOS
    for x in range(len(videos)):
        print(numcols * "-")
        indice = colored(str(x), 'green', attrs=['bold', 'dark'])
        imprimir = indice + ": " + videos[x]
        if leer_settings("oneline") == 1:
            #El 17 extra es porque al parecer los colores de termcolor agregan esa longitud al string
            imprimir = imprimir[:numcols + 17]
        print(imprimir)

    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))
    print(colored(numcols*"=", 'red', attrs=['bold', 'dark']))
    print(leer_settings("ruta_carpeta"))
    print(colored(numcols*"=", 'red', attrs=['bold', 'dark']))

    i = menu(numcols)
    if i[0] == "menu":
        return ["pelicula","carpeta","palabras","resultados","configuracion","ayuda","acerca_de", "salir"][i[1]]
    else:
        #Verifica que se haya ingresado un valor numérico y que la opcion de película exista
        if len([x for x in i[1] if x in "0123456789"]) == len(i[1]):
            if int(i[1]) < len(videos):
                editar_settings("video", videos[int(i[1])])
                editar_settings("ruta_video", leer_settings("ruta_carpeta"))
                return "palabras"
        return "pelicula"

