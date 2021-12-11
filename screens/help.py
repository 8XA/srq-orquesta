#!/bin/env python

from modules.columns_number import columns_number_func
from modules.viewer import visor
from modules.admin_db import read_settings, edit_settings
from modules.menu import menu

def help_section():
    if read_settings("menu") not in [6,7]:
        edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","6")
    numcols = columns_number_func()

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
            2: "folder",
            3: "words",
            4: "results",
            5: "settings",
            }

    menu_anterior = read_settings("previous_menu")
    visor(titulos[menu_anterior], archivo[menu_anterior])

    return read_settings("previous_menu")

