#!/bin/env python

from termcolor import colored
from modulos.numcols import num_cols
from modulos.menu import menu
from modulos.fit_frases import fit_frase


def visor(titulo, archivo):
    numcols = num_cols()
    ruta = "/data/data/com.termux/files/usr/share/sub4time/sub4time/imprimibles/"

    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])

    print(linea_azul)
    print(((numcols - len(titulo))//2) * " " + titulo)
    print(linea_azul)
    print(linea_roja)

    with open(ruta + archivo, "r") as texto:
        doc = texto.readlines()

    imprimir = ''
    for renglon in doc:
        #imprimir += renglon
        imprimir += fit_frase(numcols, renglon)

    print(imprimir)

    print(linea_roja)
    i = menu(numcols)
    
    print(doc)




#
#
#
#    editar_settings("menu_anterior", str(leer_settings("menu")))
#    editar_settings("menu","2")
#    extensiones = leer_settings("extensiones").split(',')
#    video = leer_settings("video")
#    numcols = num_cols()
#
#    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
#    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
#
#    titulo = "PALABRAS DE BÚSQUEDA"
#    print(linea_azul)
#    print(((numcols - len(titulo))//2) * " " + titulo)
#    print(linea_azul)
#
#    if leer_settings("video") == "":
#        msj = "Aquí aparecerán palabras de búsqueda sugeridas " + \
