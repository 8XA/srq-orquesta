#!/bin/env python

from termcolor import colored
from modules.columns_number import columns_number_func
from modules.files_from_route import videos_en_ruta
from modules.admin_db import read_settings, edit_settings, \
read_simple_list, edit_simple_list
from modules.menu import menu
from modules.strings_fitting import phrase_fitting, centered_phrase_fitting
import os

def videos():
    numcols = columns_number_func()
    titulo = "SRQ ORQUESTA"

    rutas_y_videos = videos_en_ruta()
    filtro = " ".join(read_settings("videos_filter").split(",")).split(" ")
    videos = rutas_y_videos[1]
    rutas = rutas_y_videos[0]
    
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","videos")

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
    played_videos = read_simple_list("played_videos")
    for x in range(len(videos)):
        #Aplica filtro
        if len([palabra for palabra in filtro if palabra \
                in videos[x].lower()]) == len(filtro):

            print(numcols * "-")

            #Marca el video seleccionado actual
            if (read_settings("selected_video_route") != "") and \
               (read_settings("selected_video_route") == rutas[x]) and \
               (read_settings("selected_video_name") == videos[x]):

                marca_en_pantalla = True
                indice_marcado = x
                indice = colored(str(x), 'green', 'on_white', attrs=['bold', 'dark'])
            else:
                indice = colored(str(x), 'green', attrs=['bold', 'dark'])

            imprimir = videos[x]
            if read_settings("one_line") == 1:
                imprimir = imprimir[:numcols - len(str(x)) -2]

            if rutas[x] + videos[x] in played_videos:
                imprimir = colored(imprimir, 'red', 'on_yellow', attrs=['bold'])

            print(indice + ": " + imprimir)
    if len(videos) == 0:
        msj = "Nada para mostrar. Prueba con otra carpeta..."
        print(numcols * "-")
        print("\n")
        print(phrase_fitting(numcols, msj))
        print("\n")

    print(linea_azul)
    print(linea_roja)
    print(colored(centered_phrase_fitting(numcols, "Ruta:"), 'white', attrs=['bold']))
    print(read_settings("folder_route"))
    print(linea_roja)
    print(colored(centered_phrase_fitting(numcols, "Filtros:"), 'white', attrs=['bold']))
    print(centered_phrase_fitting(numcols, " ".join(filtro)))
    print(linea_roja)

    i = menu(numcols, "Filtra o selecciona un video")

    if type(i[1]) is str:
        valor_numerico = ((len([x for x in i[1] if x in "0123456789"]) == len(i[1])) and (i[1] != ""))

    if i[0] == "menu":
        return i[1]
    elif (marca_en_pantalla) and ((i[1] == "")):
        return 'words'
    elif i[1].lower() == 'clean':
        edit_simple_list('played_videos')
    elif i[1].lower() == 'm':
        selected_video = read_settings('selected_video_route') + \
                read_settings('selected_video_name')
        if selected_video in played_videos:
            edit_simple_list('played_videos', selected_video)
        else:
            edit_simple_list('played_videos', selected_video, 'add')
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
    return 'videos'

