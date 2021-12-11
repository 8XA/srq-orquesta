#!/bin/env python

from termcolor import colored
from modules.columns_number import columns_number_func
from modules.files_from_route import videos_en_ruta
from modules.admin_db import read_settings, edit_settings
from modules.menu import menu
from modules.strings_fitting import fit_frase, fit_frase_centrada
import os

def videos():
    numcols = columns_number_func()
    titulo = "SRQ ORQUESTA"

    rutas_y_videos = videos_en_ruta()
    filtro = " ".join(read_settings("videos_filter").split(",")).split(" ")
    videos = rutas_y_videos[1]
    rutas = rutas_y_videos[0]
    
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","1")

    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
    titulo_colored = colored(titulo, 'red', attrs=['bold', 'dark'])


    marca_en_pantalla = False
    indice_marcado = -1

    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo_colored)
    print(linea_azul)

    print(((numcols-14)//2)*" " + "Elige un video")

    #IMPRIME NOMBRES DE VIDEOS
    for x in range(len(videos)):
        #Aplica filtro
        if len([palabra for palabra in filtro if palabra \
                in videos[x].lower()]) == len(filtro):

            print(numcols * "-")

            #Marca el video seleccionado actual
            if (read_settings("selected_video_route") != "") and \
               (read_settings("selected_video_route") == rutas[x]) and \
               (read_settings("selected_video_name") == videos[x]):

                marca_en_pantalla, indice_marcado = True, x
                indice = colored(str(x), 'green', 'on_white', attrs=['bold', 'dark'])
            else:
                indice = colored(str(x), 'green', attrs=['bold', 'dark'])

            imprimir = indice + ": " + videos[x]
            if read_settings("one_line") == 1:
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
    print(colored(fit_frase_centrada(numcols, "Ruta:"), 'white', attrs=['bold']))
    print(read_settings("folder_route"))
    print(linea_roja)
    print(colored(fit_frase_centrada(numcols, "Filtros:"), 'white', attrs=['bold']))
    print(fit_frase_centrada(numcols, " ".join(filtro)))
    print(linea_roja)

    i = menu(numcols, "Filtra o selecciona un video")

    if type(i[1]) is str:
        valor_numerico = ((len([x for x in i[1] if x in "0123456789"]) == len(i[1])) and (i[1] != ""))

    if i[0] == "menu":
        return i[1]
    elif (marca_en_pantalla) and ((i[1] == "")):
        return 3
    else:
        #Registrar opción
        if (
            #Es valor numérico
            valor_numerico and \

            #Esta dentro del rango de opciones
            (int(i[1]) < len(videos))):

            edit_settings("sub_search_changed", "1")
            edit_settings("selected_video_name", videos[int(i[1])])
            edit_settings("sub_words", "")
            edit_settings("selected_video_route", rutas[int(i[1])])

        elif i[1] != "":
            edit_settings("videos_filter", i[1].lower())
        return 1

