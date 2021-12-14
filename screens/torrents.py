#!/bin/env python 

from os import system
from termcolor import colored
from modules.menu import menu
from modules.scrapers.torrents.tpb import tpb
from modules.admin_db import read_settings, edit_settings
from modules.columns_number import columns_number_func
from modules.strings_fitting import centered_phrase_fitting

def torrents():
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","torrents")

    columns_number = columns_number_func()
    rpp = read_settings("results_per_page")
    system("clear")

    red_line = colored(columns_number*"=", 'red', attrs=['bold', 'dark'])
    yellow_line = colored(columns_number*"=", 'yellow', attrs=['bold', 'dark'])
    blue_line = colored(columns_number*"=", 'blue', attrs=['bold', 'dark'])

    titulo = "TORRENTS"
    print(blue_line)
    print(((columns_number-len(titulo))//2)*" " + titulo)
    print(blue_line)
    
    #lista_resultados = tpb(i)
    
    print(yellow_line)

    print(yellow_line)
    #Imprime filtros
    print(red_line)
    print(colored(centered_phrase_fitting(columns_number, "Filtros:"), 'white', attrs=['bold']))
    print(red_line)

    i = menu(columns_number, "Busca, filtra o elige un torrent")

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



