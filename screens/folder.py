#!/bin/env python

#Con esta pantalla puedes navegar entre las carpetas
#para seleccionar una nueva ruta de búsqueda de videos

import os
from termcolor import colored
from modules.admin_db import read_settings, edit_settings
from modules.columns_number import columns_number_func
from modules.menu import menu
from modules.strings_fitting import *

def folder():
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","2")

    ruta = read_settings("folder_route")
    cadena = [carpeta for carpeta in ruta.split("/") if carpeta != ""]

    filtros_str = " "
    while filtros_str != "":
        numcols = columns_number_func()
        linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
        linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])


        titulo = "SELECCIÓN DE CARPETA"
        print(linea_azul)
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)

        #Imprime carpetas e indices
        carpetas = sorted([carpeta.path.split("/")[-1:][0] for \
                carpeta in os.scandir(ruta) if carpeta.is_dir()])

        filtros_str = " ".join(filtros_str.lower().split(","))
        filtros = filtros_str.split(" ")
        for x in range(len(carpetas)):
            if len([filtro for filtro in filtros if filtro in \
                    carpetas[x].lower()]) == len(filtros):

                indice = colored(str(x), 'green', attrs=['bold', 'dark'])

                #Recorta el renglon si está activado "oneline" en settings
                if read_settings("one_line") == 1:
                    print(indice + ":",carpetas[x][:numcols - len(str(x)) - 2])
                else:
                    print(indice + ":",carpetas[x])

        if len(carpetas) == 0:
            msj = "Fin de la ruta, no hay más carpetas adelante..."
            print("\n")
            print(fit_frase(numcols, msj))
            print("\n")

        print(linea_azul)

        #Ruta actual en franja roja
        print(linea_roja)
        print(colored(fit_frase_centrada(numcols, "Ruta editable:"), 'white', attrs=['bold']))
        print(ruta)
        print(linea_roja)
        #Filtros
        print(colored(fit_frase_centrada(numcols, "Filtros:"), 'white', attrs=['bold']))
        print(fit_frase_centrada(numcols, filtros_str))
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
                return 1

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
                filtros_str = i[1]
