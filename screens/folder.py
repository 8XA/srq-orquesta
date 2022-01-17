#!/bin/env python

#Con esta pantalla puedes navegar entre las carpetas
#para seleccionar una nueva ruta de búsqueda de videos

import os
from subprocess import Popen, PIPE
from termcolor import colored
from modules.admin_db import edit_simple_list
from modules.refresh_history import refresh_history
from modules.admin_db import read_settings, edit_settings
from modules.columns_number import columns_number_func
from modules.menu import menu
from modules.strings_fitting import phrase_fitting, \
        centered_phrase_fitting, colored_centered_filter

def folder():
    refresh_history('folder_history')
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","folder")

    ruta = read_settings("folder_route")
    cadena = [carpeta for carpeta in ruta.split("/") if carpeta != ""]

    filtros_str = " "
    while filtros_str != "":
        numcols = columns_number_func()
        linea_amarilla = colored(numcols*"=", 'yellow', attrs=['bold', 'dark'])
        linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
        linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])


        titulo = "SELECCIÓN DE CARPETA"
        print(linea_azul)
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)

        print(linea_amarilla)

        #Imprime carpetas e indices
        bash_route = "$'" + ruta.replace("'", "\\'") + "'"
        raw_content = Popen('ls -L ' + bash_route, shell=True, stdout=PIPE, stderr=PIPE)
        dirty_folders = str(raw_content.stdout.read())[2:-1].split('\\n')

        carpetas = []
        for folder in dirty_folders:
            folder_route = "$'" + (ruta + '/' + folder + '/').replace("'","\\'") + "'"
            folder_command = Popen('ls -L ' + folder_route, shell=True, stdout=PIPE, stderr=PIPE)
            if str(folder_command.stderr.read()) == "b''" and folder != "":
                carpetas.append(folder)
        carpetas = sorted(carpetas, key=str.casefold)

        filtros_str = " ".join(filtros_str.lower().split(","))
        filtros = filtros_str.split(" ")
        while '' in filtros:
            filtros.remove('')

        show_message = False
        for x in range(len(carpetas)):
            if len([filtro for filtro in filtros if filtro in \
                    carpetas[x].lower()]) == len(filtros):

                indice = colored(str(x), 'green', attrs=['bold', 'dark'])

                #Recorta el renglon si está activado "oneline" en settings
                if read_settings("one_line") == 1:
                    print(indice + ":",carpetas[x][:numcols - len(str(x)) - 2])
                else:
                    print(indice + ":",carpetas[x])
                show_message = True

        if len(carpetas) == 0:
            msj = "Fin de la ruta, no hay más carpetas adelante..."
        elif show_message == False:
            msj = "Prueba con otro filtro..."
        if show_message == False or len(carpetas) == 0:
            print("\n")
            print(phrase_fitting(numcols, msj))
            print("\n")

        print(linea_amarilla)

        #Ruta actual en franja roja
        print(linea_roja)
        print(colored(centered_phrase_fitting(numcols, "Ruta editable:"), 'white', attrs=['bold']))
        print(ruta)
        print(linea_roja)
        #Filtros
        print(colored(centered_phrase_fitting(numcols, "Filtros:"), 'white', attrs=['bold']))
        colored_filters = colored_centered_filter(numcols, \
                "  ".join(filtros))
        if len(filtros) > 0:
            print(colored_filters)
        print(linea_roja)

        i = menu(numcols, "Define la carpeta de búsqueda")

        #Ejecuta una acción dependiendo del comando ingresado
        if i[0] == "menu":
            return i[1]
        else:
            if i[1] == "":
                if read_settings("folder_route") != ruta:
                    edit_settings("videos_filter", "")
                    edit_settings("folder_route", ruta)
                return 'videos'

            elif (i[1].isdigit()) and (len(carpetas) > int(i[1])):
                cadena.append(carpetas[int(i[1])])
                ruta = "/" + "/".join(cadena) + "/"
                filtros_str = " "

            elif i[1] == "..":
                if len(cadena) > 1:
                    cadena.pop()
                    filtros_str = " "
                ruta = "/" + "/".join(cadena) + "/"
            else:
                edit_simple_list('folder_history', i[1], 'add')
                filtros_str = i[1]
