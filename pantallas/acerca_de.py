#!/bin/env python

from modulos.numcols import num_cols
from modulos.viewer import visor
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu

def acerca_de():
    if leer_settings("menu") not in [6,7]:
        editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","7")
    numcols = num_cols()

    visor("ACERCA DE", "acerca_de")
    visor("NOVEDADES DE LA VERSIÓN", "actualizacion")

    return leer_settings("menu_anterior")
