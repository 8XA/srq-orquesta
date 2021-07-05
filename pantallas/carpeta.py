#!/bin/env python

#Con esta pantalla puedes navegar entre las carpetas
#para seleccionar una nueva ruta de búsqueda de videos

import os
from termcolor import colored
from modulos.admindb import leer_settings, editar_settings
from modulos.numcols import num_cols
from modulos.menu import menu
from modulos.fit_frases import fit_frase

def carpeta():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","1")
    numcols = num_cols()

    ruta = leer_settings("ruta_carpeta")
    cadena = [carpeta for carpeta in ruta.split("/") if carpeta != ""]

    accion = "."
    while accion != "":
        os.system("clear")
        linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
        linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])


        titulo = "SELECCIÓN DE CARPETA"
        print(linea_azul)
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)

        #Imprime carpetas e indices
        carpetas = sorted([carpeta.path.split("/")[-1:][0] for \
                carpeta in os.scandir(ruta) if carpeta.is_dir()])

        for x in range(len(carpetas)):
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
        print(ruta)
        print(linea_roja)

        i = menu(numcols)

        #Ejecuta una acción dependiendo del comando ingresado
        if i[0] == "menu":
            return i[1]
        else:
            accion = i[1]
            if accion == "":
                editar_settings("ruta_carpeta", ruta)
                return leer_settings("menu_anterior")

            elif "".join([x for x in accion if x in "0123456789"]) == accion:
                if len(carpetas) > int(accion) >= 0:
                    cadena.append(carpetas[int(accion)])
                    ruta = "/" + "/".join(cadena) + "/"

            elif accion == "..":
                if len(cadena) > 1:
                    cadena.pop()
                ruta = "/" + "/".join(cadena) + "/"
            else:
                pass
