#!/bin/env python

from modules.columns_number import columns_number_func
from modules.viewer import visor
from modules.admin_db import read_settings, edit_settings
from modules.menu import menu

def help_section():
    if read_settings("menu") not in ['help_section','about']:
        edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","help_section")
    numcols = columns_number_func()

    titulos = {
        'torrents': "AYUDA: BÚSQUEDA Y DESCARGA DE TORRENTS",
        'videos': "AYUDA: SELECCIÓN DE VIDEO",
        'folder': "AYUDA: SELECCIÓN DE CARPETA",
        'words': "AYUDA: PALABRAS DE BÚSQUEDA",
        'results': "AYUDA: RESULTADOS",
        'settings': "AYUDA: CONFIGURACIÓN",
    }

    menu_anterior = read_settings("previous_menu")
    visor(titulos[menu_anterior], menu_anterior)

    return read_settings("previous_menu")

