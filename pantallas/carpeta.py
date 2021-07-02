#!/bin/env python

import os
from termcolor import colored
from modulos.admindb import leer_settings, editar_settings
from modulos.numcols import num_cols
from modulos.menu import menu

def carpeta():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","1")
    ruta = leer_settings("ruta_carpeta").split("/")
    numcols = num_cols()

    accion = "."
    while accion != "":
        os.system("clear")
        linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
        linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])


        titulo = "SELECCIÓN DE CARPETA"
        print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)

        carpetas = sorted([x.path.split("/")[-1:][0] for x in os.scandir("/".join(ruta)) if x.is_dir()])
        
        for x in range(len(carpetas)):
            indice = colored(str(x), 'green', attrs=['bold', 'dark'])
            print(indice + ":",carpetas[x])
        print(linea_azul)
        print(linea_roja)
        print("storage/" + "/".join(ruta[8:]))
        print(linea_roja)

        i = menu(numcols)

        print(linea_azul)
        

        if i[0] == "menu":
            return ["pelicula","carpeta","palabras","resultados","configuracion","ayuda","acerca_de", "salir"][i[1]]
        else:
            if accion == "":
                editar_settings("ruta_carpeta", "/".join(ruta))
                return ["pelicula","carpeta","palabras","resultados","configuracion","ayuda","acerca_de", "salir"][leer_settings("menu_anterior")]
            elif "".join([x for x in accion if x in "0123456789"]) == accion:
                if len(carpetas) > int(accion) >= 0:
                    ruta.append(carpetas[int(accion)])
            elif accion == "..":
                if len(ruta) > 8:
                    ruta.pop()
            else:
                pass

