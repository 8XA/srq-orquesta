#!/bin/env python

import os
from termcolor import colored
from modulos.numcols import num_cols
from modulos.admindb import leer_settings, editar_settings

def carpeta():
    numcols = num_cols()
    ruta = leer_settings("ruta_carpeta")

    accion = "."
    while accion != "":
        os.system("clear")
        titulo = "SELECCIÓN DE CARPETA"
        print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))
        print("storage/" + "/".join(ruta[8:]) + "\n")

        carpetas = sorted([x.path.split("/")[-1:][0] for x in os.scandir("/".join(ruta)) if x.is_dir()])
        
        for x in range(len(carpetas)):
            indice = colored(str(x), 'green', attrs=['bold', 'dark'])
            print(indice + ":",carpetas[x])
        print(colored(numcols*"-", 'blue', attrs=['bold', 'dark']))
        indice = colored("..", 'green', attrs=['bold', 'dark'])
        print(indice + ": Directorio anterior")
        indice = colored("Enter", 'green', attrs=['bold', 'dark'])
        print(indice + ": Aceptar")

        print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))
        accion = input(": ")
        
        if accion == "":
            editar_settings("ruta_carpeta", "/".join(ruta))
            return "pelicula"
        elif "".join([x for x in accion if x in "0123456789"]) == accion:
            if len(carpetas) > int(accion) >= 0:
                ruta.append(carpetas[int(accion)])
        elif accion == "..":
            if len(ruta) > 8:
                ruta.pop()
        else:
            pass

