#!/bin/env python 

import os
from termcolor import colored
from modules.menu import menu
from modules.scrapers.torrents.tpb import tpb
from modules.admin_db import read_settings, edit_settings
from modules.columns_number import columns_number_func
from modules.strings_fitting import *

def torrents():
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","torrents")

    numcols = columns_number_func()
    rpp = read_settings("results_per_page")
    os.system("clear")

    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
    linea_amarilla = colored(numcols*"=", 'yellow', attrs=['bold', 'dark'])
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])

    titulo = "TORRENTS"
    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo)
    print(linea_azul)
    
    #lista_resultados = tpb(i)
    
    print(linea_amarilla)

    print(linea_amarilla)
    #Imprime filtros
    print(linea_roja)
    print(colored(fit_frase_centrada(numcols, "Filtros:"), 'white', attrs=['bold']))
    print(linea_roja)

    i = menu(numcols, "Busca, filtra o elige un torrent")

    #Si es alguna pantalla del menu
    if i[0] == "menu":
        return i[1]
    else:
        return 'torrents'

#torrents
#marcado de torrents descargados
#Enter envía a cliente torrent y pasa a pantalla videos
#ID titulo peso
#seeds
#leechers
#procedencia
#
#
#acciones: enter para descargar y pasar a palabras
#Filtros
#

#lee base de datos, la base de datos tiene lista de torrents:
#titulo  peso seeds leeches  procedencia magnetlink



