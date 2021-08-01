#!/bin/env python

from termcolor import colored
from modulos.numcols import num_cols
from modulos.menu import menu
from modulos.fit_frases import fit_frase


def visor(titulo, archivo):
    numcols = num_cols()
    ruta = "/data/data/com.termux/files/usr/share/apocalipsis-orquesta/apocalipsis-orquesta/imprimibles/"

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
        imprimir += fit_frase(numcols, renglon)
        imprimir += "\n"
    print(imprimir)

    print(linea_roja)

    return 0
