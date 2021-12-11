#!/bin/env python

from modules.columns_number import columns_number_func
from modules.viewer import visor
from modules.admin_db import read_settings, edit_settings
from modules.menu import menu

def acerca_de():
    if read_settings("menu") not in [6,7]:
        edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","7")
    numcols = columns_number_func()

    visor("ACERCA DE", "about","update")

    return read_settings("previous_menu")
