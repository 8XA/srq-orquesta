#!/bin/env python

from modules.columns_number import columns_number_func
from modules.viewer import viewer
from modules.admin_db import read_settings, edit_settings
from modules.menu import menu

def about():
    if read_settings("menu") not in ['help_section','about']:
        edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","about")
    numcols = columns_number_func()

    viewer("ACERCA DE", "about","update")

    return read_settings("previous_menu")
