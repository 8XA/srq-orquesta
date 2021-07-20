#!/bin/env python 

from modulos.numcols import num_cols
from modulos.admindb import leer_settings, editar_settings
from modulos.fit_frases import *
from termcolor import colored
import time

def una_sesion():
    numcols = num_cols()

    linea_azul_ = colored(numcols*"-", 'blue', attrs=['bold', 'dark'])
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    cero_verde = colored("0", 'green', attrs=['bold','dark'])
    uno_verde = colored("1", 'green', attrs=['bold','dark'])

    print(linea_azul)
    msj = "Sub4Time está actualmente en ejecución o no se cerró correctamente. " + \
            "Tener más de una instancia abierta puede provocar un comportamiento inesperado."

    opciones = uno_verde + ": Sí\n" + cero_verde + ": No\n"
    print(fit_frase(numcols, msj))
    print(linea_azul_)
    print(colored(fit_frase_centrada(numcols, "Desea forzar inicio?"), 'white', attrs=['bold']))
    print(linea_azul_)
    imprimir = opciones + linea_azul + "\n: "
    i = input(imprimir)

    if i.isdigit() and int(i) == 1:
        editar_settings("instancia_activa", "0")
        
        print("\nForzando apertura. Inicia de nuevo...")
        time.sleep(1)
