#!/bin/env python

#Con esta pantalla puedes navegar entre las carpetas
#para seleccionar una nueva ruta de búsqueda de videos

import os
from termcolor import colored
from modulos.admindb import leer_settings, editar_settings
from modulos.numcols import num_cols
from modulos.menu import menu
from modulos.fit_frases import *

def carpeta():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","1")

    ruta = leer_settings("ruta_carpeta")
    cadena = [carpeta for carpeta in ruta.split("/") if carpeta != ""]

    filtros_str = " "
    while filtros_str != "":
        numcols = num_cols()
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
                if leer_settings("oneline") == 1:
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
        print(colored(fit_frase_centrada(numcols, "Ruta:"), 'white', attrs=['bold']))
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
                editar_settings("ruta_carpeta", ruta)
                return leer_settings("menu_anterior")

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
