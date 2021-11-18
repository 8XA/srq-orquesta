#!/bin/env python

from modulos.numcols import num_cols
from modulos.viewer import visor
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu

def ayuda():
    if leer_settings("menu") not in [6,7]:
        editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","6")
    numcols = num_cols()

    titulos = {
            0: "AYUDA: BÚSQUEDA Y DESCARGA DE TORRENTS",
            1: "AYUDA: SELECCIÓN DE VIDEO",
            2: "AYUDA: SELECCIÓN DE CARPETA",
            3: "AYUDA: PALABRAS DE BÚSQUEDA",
            4: "AYUDA: RESULTADOS",
            5: "AYUDA: CONFIGURACIÓN",
            }

    archivo = {
            0: "torrents",
            1: "videos",
            2: "carpeta",
            3: "palabras",
            4: "resultados",
            5: "configuracion",
            }

    menu_anterior = leer_settings("menu_anterior")
    visor(titulos[menu_anterior], archivo[menu_anterior])

    return leer_settings("menu_anterior")

