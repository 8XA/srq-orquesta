#!/bin/env python 

from modules.columns_number import columns_number_func
from modules.admin_db import edit_settings
from modules.strings_fitting import *
from termcolor import colored
import time

def una_sesion():
    numcols = columns_number_func()

    linea_azul_ = colored(numcols*"-", 'blue', attrs=['bold', 'dark'])
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    cero_verde = colored("0", 'green', attrs=['bold','dark'])
    uno_verde = colored("1", 'green', attrs=['bold','dark'])

    print(linea_azul)
    msj = "SRQ ORQUESTA está actualmente en ejecución o no se cerró correctamente. " + \
            "Tener más de una instancia abierta puede provocar un comportamiento inesperado."

    opciones = uno_verde + ": Sí\n" + cero_verde + ": No\n"
    print(fit_frase(numcols, msj))
    print(linea_azul_)
    print(colored(fit_frase_centrada(numcols, "Desea forzar inicio?"), 'white', attrs=['bold']))
    print(linea_azul_)
    imprimir = opciones + linea_azul + "\n: "
    i = input(imprimir)

    if i.isdigit() and int(i) == 1:
        edit_settings("active_instance", "0")
        
        print("\nForzando apertura. Inicia de nuevo...")
        time.sleep(1)
