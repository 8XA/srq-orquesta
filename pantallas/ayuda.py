#!/bin/env python

from modulos.numcols import num_cols
from modulos.text_viewer import visor
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu

def ayuda():
    if leer_settings("menu") not in [6,7]:
        editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","6")
    numcols = num_cols()

    titulos = {
            1: "AYUDA: VIDEOS",
            2: "AYUDA: CARPETA",
            3: "AYUDA: PALABRAS",
            4: "AYUDA: RESULTADOS",
            5: "AYUDA: CONFIGURACIÓN",
            }

    archivo = {
            1: "videos",
            2: "carpeta",
            3: "palabras",
            4: "resultados",
            5: "configuracion",
            }

    menu_anterior = leer_settings("menu_anterior")
    visor(titulos[menu_anterior], archivo[menu_anterior])

    i = menu(numcols, "Navega por el menú o regresa")
    if i[0] == "menu":
        return i[1]

    return leer_settings("menu_anterior")




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
