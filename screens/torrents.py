#!/bin/env python 

import os
from termcolor import colored
from modulos.menu import menu
from modulos.scrapers.torrents.tpb import tpb
from modulos.admindb import leer_settings, editar_settings
from modulos.numcols import *
from modulos.fit_frases import *

def torrents():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","0")

    numcols = num_cols()
    rpp = leer_settings("rpp")
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
        return 0

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



