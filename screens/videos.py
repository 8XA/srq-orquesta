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
from multiprocessing import Process
import sys


def refresh_videos(videos_list):

    videos_and_routes = videos_list
    updated_videos = videos_en_ruta()
    while videos_and_routes == updated_videos:
        updated_videos = videos_en_ruta()
        sleep(0.01)

    good = False
    while not good:
        try:
            #Changing the selected video
            if len(updated_videos[1]) > len(videos_and_routes[1]) and \
                    read_settings("select_refreshed_video") == 1:

                edit_settings("select_refreshed_video", "0") 
                edit_settings("sub_search_changed", "1")
                edit_settings("sub_words", "")

                full_routes = [videos_and_routes[0][indx] + \
                        videos_and_routes[1][indx] for indx in range(len(videos_and_routes[1]))]

                new_videos = [[updated_videos[0][indx], updated_videos[1][indx]] for indx in \
                        range(len(updated_videos[1])) if updated_videos[0][indx] + \
                        updated_videos[1][indx] not in full_routes]

                #Select the video
                v_dict = {}
                for indx in range(len(new_videos)):
                    v_dict[new_videos[indx][1] + "_" + str(indx)] = new_videos[indx][0]
                ordered = sorted([video for video in v_dict], key=str.casefold)
                
                video = ordered[0][:ordered[0].rindex("_")] 
                route = v_dict[ordered[0]]

                edit_settings("selected_video_name", video)
                edit_settings("selected_video_route", route)

                filters = [vfilter for vfilter in " ".join(read_settings("videos_filter").split(",")).split(" ") \
                        if vfilter != '']
                plus_filter = []
                minus_filter = []

                for filter_ in filters:
                    if len(filter_) > 1 and filter_[0] == '-':
                        minus_filter.append(filter_)
                    else:
                        plus_filter.append(filter_)

                if not (len([filter_ for filter_ in plus_filter if filter_.lower() in \
                        video.lower()]) == len(plus_filter) and len([filter_ for filter_ in \
                        minus_filter if filter_[1:].lower() in video.lower()]) == 0):
                    edit_settings("videos_filter", "")

            #Restart SRQ
            edit_settings("dimention_status", "refresh") 
            good = True

        except:
            pass
    
def videos():
    rutas_y_videos = videos_en_ruta()

    #Parallel processes
    cleaning = Process(
            target=subs_and_folders_deletion
            #daemon=True
        )
    refresh_process = Process(
            target=refresh_videos,
            args=[rutas_y_videos]
            #daemon=True
        )
    refresh_process.start()
    cleaning.start()

    refresh_history('videos_history')
    numcols = columns_number_func()

    titulo = "<- SRQ ORQUESTA ->"

    filters = " ".join(read_settings("videos_filter").split(",")).split(" ")
    plus_filter = []
    minus_filter = []

    for filter_ in filters:
        if filter_ != '':
            if len(filter_) > 1 and filter_[0] == '-':
                minus_filter.append(filter_)
            else:
                plus_filter.append(filter_)

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
        if len([palabra for palabra in plus_filter if palabra.lower() in \
                videos[x][:videos[x].rindex("_")].lower()]) == len(plus_filter) and \
                len([palabra for palabra in minus_filter if palabra[1:].lower() in \
                videos[x][:videos[x].rindex("_")].lower()]) == 0:

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
        if len(plus_filter + minus_filter) > 0:
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
            "  ".join(plus_filter + minus_filter))
    
    if len(plus_filter + minus_filter) > 0:
        print(colored_filters)

    print(linea_roja)

    i = menu(numcols, "Filtra o selecciona un video")
    cleaning.kill()
    refresh_process.kill()

    if i[0] == "menu":
        return i[1]

    #Sends you to 'Palabras'
    elif (marca_en_pantalla) and ((i[1] == "")):
        return 'words'

    elif i[1] == "":
        return 'videos'

    #Clean the video marks
    elif i[1].lower() == 'clean':
        edit_simple_list('played_videos')

    #Mark the selected video
    elif i[1].lower() == 'm':
        selected_video = read_settings('selected_video_route') + \
                read_settings('selected_video_name')
        selected_video = selected_video.replace("\\'","\'")
        if selected_video in played_videos:
            edit_simple_list('played_videos', selected_video)
        else:
            edit_simple_list('played_videos', selected_video, 'add')

    #Mark a video
    elif i[1][-1].lower() == 'm' and i[1][:-1].isdigit():
        video_name = videos[int(i[1][:-1])][:videos[int(i[1][:-1])].rindex("_")]
        route_name = rutas[videos[int(i[1][:-1])]]

        if route_name + video_name in played_videos:
            edit_simple_list('played_videos', route_name + video_name)
        else:
            edit_simple_list('played_videos', route_name + video_name, 'add')

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

    #Play a video
    elif (
        #Las character is a 'p'
        i[1][-1].lower() == 'p' and \

        #It is a number value 
        i[1][:-1].isdigit() and \

        #It is in a valid range
        (int(i[1][:-1]) < len(videos))):
        video_name = videos[int(i[1][:-1])][:videos[int(i[1][:-1])].rindex("_")]
        route_name = rutas[videos[int(i[1][:-1])]]
        edit_settings("sub_search_changed", "1")
        edit_settings("selected_video_name", video_name)
        edit_settings("selected_video_route", route_name)
        edit_settings("sub_words", "")
        edit_simple_list('played_videos', route_name + video_name, 'add')

        Popen(["xdg-open", route_name + video_name], stdout=PIPE, stderr=PIPE).wait()

    #Videos deletion
    elif any([
        i[1].lower() == 'd',
        i[1].lower() == 'dm',

        len(i[1]) > 1 and \
        i[1][-1].lower() == 'd' and \
        i[1][:-1].isdigit() and \
        int(i[1][:-1]) < len(videos)
        ]):

        if i[1].lower() == 'd':
            str_deletion = "el video '" + read_settings("selected_video_name") + "'"
        elif i[1].lower() == 'dm':
            str_deletion = "los videos filtrados marcados"
        else:
            str_deletion = "el video '" + videos[int(i[1][:-1])][:videos[int(i[1][:-1])].rindex("_")] + "'"

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
                    to_delete = rutas[videos[int(i[1][:-1])]] + \
                            videos[int(i[1][:-1])][:videos[int(i[1][:-1])].rindex("_")]
                to_delete = to_delete.replace("\\'", "'")

                if Path(to_delete).is_file():
                    deletion = Popen(["rm", "-f", to_delete], stderr=PIPE, stdout=PIPE)
                else:
                    Popen("clear").wait()
                    print(phrase_fitting(numcols, "El video no existe..."))
                    sleep(0.05)

            #Delete the marked videos
            else:
                for to_delete in marked_video_list:
                    deletion = Popen(["rm", "-f", to_delete], stderr=PIPE, stdout=PIPE)

    #Set a filter
    elif i[1] != "":
        edit_simple_list('videos_history', i[1], 'add')
        edit_settings("videos_filter", i[1].lower())

    return 'videos'

