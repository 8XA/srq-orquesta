#!/bin/env python

from modulos.numcols import num_cols
from modulos.text_viewer import visor
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu

def acerca_de():
    if leer_settings("menu") not in [5,6]:
        editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","6")
    numcols = num_cols()

    visor("ACERCA DE", "acerca_de")

    i = menu(numcols)
    if i[0] == "menu":
        return i[1]

    elif i[1] == "":
        return leer_settings("menu_anterior")
    else:
        return 6
        
