#!/bin/env python

import os
from modulos.admindb import leer_settings

def descarga():
    os.system("clear")    
    print("... aqui va el proceso de descarga...")
    print(leer_settings("link_descarga"))
    input()
    return 3
