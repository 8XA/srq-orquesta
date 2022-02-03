#!/bin/env python

from termcolor import colored
from modules.folders_clean import subs_and_folders_deletion
from modules.refresh_history import refresh_history
from modules.columns_number import columns_number_func
from modules.files_from_route import videos_en_ruta
from modules.admin_db import read_settings, edit_settings, \
read_simple_list, edit_simple_list
from modules.menu import menu
from modules.strings_fitting import phrase_fitting, \
        centered_phrase_fitting, colored_centered_filter
from subprocess import Popen, PIPE
from pathlib import Path
from time import sleep
from threading import Thread
import sys
from os import execv

def videos():
    global to_return, to_refresh

    to_return = None
    to_refresh = False

    #Cleaning the old remnants
    cleaning = Thread(
            target=subs_and_folders_deletion,
            daemon=True
        )
    screen_thread = Thread(
        target=screen_and_options,
        daemon=True
        )
    refresh_thread = Thread(
        target=refresh_videos,
        daemon=True
        )
    
    cleaning.start()
    screen_thread.start()
    refresh_thread.start()

    while refresh_thread.is_alive() or screen_thread.is_alive() or cleaning.is_alive():#
        if to_refresh:
            #Restart SRQ
            edit_settings("dimention_status", "refreshing") 
            edit_settings("active_instance", "0") 
            sys.stdout.flush()
            execv(sys.argv[0], sys.argv)

        sleep(0.1)
    
    return to_return

def refresh_videos():
    global to_return, to_refresh

    videos_and_routes = videos_en_ruta()
    while videos_en_ruta() == videos_and_routes:
        if to_return != None:
            break
        sleep(0.1)

    if to_return == None:
        to_refresh = True
    
def screen_and_options():
    global to_return

    refresh_history('videos_history')
    numcols = columns_number_func()
    titulo = "<- SRQ ORQUESTA ->"

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
    titulo_colored = colored(titulo, 'red', 'on_grey', attrs=['bold'])


    marca_en_pantalla = False
    indice_marcado = -1

    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo_colored)
    print(linea_azul)

    print(((numcols-14)//2)*" " + "Elige un video")

    #IMPRIME NOMBRES DE VIDEOS
    played_videos = read_simple_list("played_videos")
    marked_video_list = []
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
                marked_video = marked_video.replace("\'","'")
                marked_video_list.append(marked_video)

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

    if i[0] == "menu":
        to_return = i[1]
        return None

    #Sends you to 'Palabras'
    elif (marca_en_pantalla) and ((i[1] == "")):
        to_return = 'words'
        return None

    #Clean the video marks
    elif i[1].lower() == 'clean':
        edit_simple_list('played_videos')

    #Mark a video
    elif i[1].lower() == 'm':
        selected_video = read_settings('selected_video_route') + \
                read_settings('selected_video_name')
        selected_video = selected_video.replace("\\'","\'")
        if selected_video in played_videos:
            edit_simple_list('played_videos', selected_video)
        else:
            edit_simple_list('played_videos', selected_video, 'add')

    #Choose a video
    elif (
        #Es valor numérico
        i[1].isdigit() and \

        #Esta dentro del rango de opciones
        (int(i[1]) < len(videos))):

        edit_settings("sub_search_changed", "1")
        edit_settings("selected_video_name", videos[int(i[1])][:videos[int(i[1])].rindex("_")])
        edit_settings("sub_words", "")
        edit_settings("selected_video_route", rutas[videos[int(i[1])]])

    #Videos deletion
    elif any([
        i[1].lower() == 'd',
        i[1].lower() == 'dm',

        len(i[1]) > 1 and \
        i[1][0].lower() == 'd' and \
        i[1][1:].isdigit() and \
        int(i[1][1:]) < len(videos)
        ]):

        if i[1].lower() == 'd':
            str_deletion = "el video '" + read_settings("selected_video_name") + "'"
        elif i[1].lower() == 'dm':
            str_deletion = "los videos filtrados marcados"
        else:
            str_deletion = "el video '" + videos[int(i[1][1:])][:videos[int(i[1][1:])].rindex("_")] + "'"

        message = phrase_fitting(numcols, "Está a punto de eliminar " + str_deletion + ". Esta acción requiere confirmación.")
        enter = colored("Enter", 'green', attrs=['bold', 'dark'])
        cancel = colored("C", 'green', attrs=['bold', 'dark'])

        enter_message = enter + ": Confirmar"
        cancel_message = cancel + ": Cancelar"

        Popen("clear").wait()
        print(linea_azul)
        print(message)
        print(numcols * "-")
        print(enter_message)
        print(cancel_message)
        print(linea_azul)

        proceed = input(": ") == ''

        if proceed:
            if i[1].lower() == 'd' or i[1].lower() != 'dm':

                #Delete the selected video
                to_delete = read_settings("selected_video_route") + read_settings("selected_video_name")
                if i[1].lower() != 'd':
                    #Delete a numbered video
                    to_delete = rutas[videos[int(i[1][1:])]] + \
                            videos[int(i[1][1:])][:videos[int(i[1][1:])].rindex("_")]
                to_delete = to_delete.replace("\\'", "'")

                if Path(to_delete).is_file():
                    deletion = Popen(["rm", "-f", to_delete], stderr=PIPE, stdout=PIPE)
                else:
                    Popen("clear").wait()
                    print(phrase_fitting(numcols, "El video no existe..."))
                    sleep(1)

            #Delete the marked videos
            else:
                for to_delete in marked_video_list:
                    deletion = Popen(["rm", "-f", to_delete], stderr=PIPE, stdout=PIPE)

    #Set a filter
    elif i[1] != "":
        edit_simple_list('videos_history', i[1], 'add')
        edit_settings("videos_filter", i[1].lower())

    to_return = 'videos'
    return None

