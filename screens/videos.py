#!/bin/env python

from termcolor import colored
from modules.refresh_history import refresh_history
from modules.columns_number import columns_number_func
from modules.files_from_route import videos_en_ruta
from modules.admin_db import read_settings, edit_settings, \
read_simple_list, edit_simple_list
from modules.menu import menu
from modules.strings_fitting import phrase_fitting, \
        centered_phrase_fitting, colored_centered_filter

def videos():
    refresh_history('videos_history')
    numcols = columns_number_func()
    titulo = "SRQ ORQUESTA"

    rutas_y_videos = videos_en_ruta()

    filtro = " ".join(read_settings("videos_filter").split(",")).split(" ")
    while '' in filtro:
        filtro.remove('')

    # Ordered videos and their routes
    videos = rutas_y_videos[1]
    rutas = {}
    for index in range(len(videos)):
        rutas[videos[index] + "_" + str(index)] = rutas_y_videos[0][index]
    videos = sorted([video for video in rutas], key=str.casefold)

    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","videos")

    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
    titulo_colored = colored(titulo, 'white', 'on_red', attrs=['bold', 'dark'])


    marca_en_pantalla = False
    indice_marcado = -1

    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo_colored)
    print(linea_azul)

    print(((numcols-14)//2)*" " + "Elige un video")

    #IMPRIME NOMBRES DE VIDEOS
    played_videos = read_simple_list("played_videos")
    filtered = False
    for x in range(len(videos)):
        #Aplica filtro
        if len([palabra for palabra in filtro if palabra \
                in videos[x][:videos[x].rindex("_")].lower()]) == len(filtro):

            print(numcols * "-")
            filtered = True

            #Marca el video seleccionado actual
            if (read_settings("selected_video_route") != "") and \
               (read_settings("selected_video_route") == rutas[videos[x]]) and \
               (read_settings("selected_video_name") == videos[x][:videos[x].rindex("_")]):

                marca_en_pantalla = True
                indice_marcado = x
                indice = colored(str(x), 'green', 'on_white', attrs=['bold', 'dark'])
            else:
                indice = colored(str(x), 'green', attrs=['bold', 'dark'])

            imprimir = videos[x][:videos[x].rindex("_")]
            if read_settings("one_line") == 1:
                imprimir = imprimir[:numcols - len(str(x)) -2]

            marked_video = rutas[videos[x]] + videos[x][:videos[x].rindex("_")]
            marked_video = marked_video.replace("\\\'","\'")
            if marked_video in played_videos:
                imprimir = colored(imprimir, 'red', 'on_yellow', attrs=['bold'])

            print(indice + ": " + imprimir)

    if not filtered:
        prueba = "otra carpeta..."
        if len(filtro) > 0:
            prueba = "otro filtro..."

        msj = "Nada para mostrar. Prueba con " + prueba
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

    colored_filters = colored_centered_filter(numcols, \
            "  ".join(filtro))
    
    if len(filtro) > 0:
        print(colored_filters)

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
        selected_video = selected_video.replace("\\'","\'")
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
            edit_settings("selected_video_name", videos[int(i[1])][:videos[int(i[1])].rindex("_")])
            edit_settings("sub_words", "")
            edit_settings("selected_video_route", rutas[videos[int(i[1])]])

        elif i[1] != "":
            edit_simple_list('videos_history', i[1], 'add')
            edit_settings("videos_filter", i[1].lower())
    return 'videos'

