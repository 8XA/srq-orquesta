#!/bin/env python

#Selecciona las palabras de busqueda o ingresa una busqueda libre

from modulos.numcols import num_cols
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu
from modulos.fit_frases import *
from termcolor import colored

def palabras():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","2")
    extensiones = leer_settings("extensiones_activas").split(',')
    video = leer_settings("video")
    numcols = num_cols()

    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])

    titulo = "PALABRAS DE BÚSQUEDA"
    print(linea_azul)
    print(((numcols - len(titulo))//2) * " " + titulo)
    print(linea_azul)

    if leer_settings("video") == "":
        msj = "Aquí aparecerán palabras de búsqueda sugeridas cuando selecciones un video..."
        print("\n")
        print(fit_frase(numcols, msj))
        print("\n")

    #Lista de palabras
    else:
        palabras_del_titulo = [palabra for palabra in " ".join(video.split(".")).split(" ") if (palabra != " " and palabra != "" and palabra.lower() not in extensiones)]

        for x in range(len(palabras_del_titulo)):
            indice = colored(str(x), 'green', attrs=['bold', 'dark'])
            print(indice + ": " + palabras_del_titulo[x])

    print(linea_azul)
    print(linea_roja)

    msj = "Aquí aparecerán las palabras de búsqueda que definas..."
    lista_palabras = leer_settings("palabras")
    if lista_palabras == "":
        print(fit_frase(numcols, msj))

    else:
        print(fit_frase_centrada(numcols, " ".join(lista_palabras.split(","))))
    print(linea_roja)

    i = menu(numcols)
    #Ejecuta una acción dependiendo del comando ingresado
    if i[0] == "menu":
        return i[1]

    else:
        #Si da enter
        if i[1] == "":
            if leer_settings("palabras") != "":
                return 3
            else:
                return 2
        #Si usas las sugerencias
        elif len([x for x in i[1] if x in "0123456789,-"]) == len(i[1]):
            pass
        #busqueda libre
        else:
            #editar_settings("palabras", ",".join([x for x in i[1].split(" ") if x != ""]))
            editar_settings("palabras", ",".join([x for x in " ".join(i[1].split(",")).split(" ") if x != ""]))
            #editar_settings("palabras", ",".join(i[1].split(" ")))
            return 2
    


