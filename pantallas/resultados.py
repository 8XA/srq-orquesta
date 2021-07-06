#!/bin/env python

#Muestra los resultados obtenidos por los scrapers
#Admite filtrado de búsqueda dentro de los subtítulos hallados
#Marca los subtítulos ya descargados
#Selecciona subtítulo deseado y pasa a la pantalla de descarga

import os
from termcolor import colored
from modulos.admindb import *
from modulos.fit_frases import *
from modulos.menu import menu
from modulos.numcols import num_cols
from modulos.scrapers.opensubtitles import opensubtitles
from modulos.scrapers.subdivx import subdivx

def resultados():
    os.system("clear")

    #Recuperar scrapers a utilizar
    scrapers = leer_settings("scrapers").split(",")

    #Evita buscar 2 veces seguidas lo mismo
    if leer_settings("cambio_busqueda") == 1:
        #Recuperar palabras de búsqueda
        palabras = leer_settings("palabras").split(",")

        #obtener subtítulos
        get_subs = {
                "opensubtitles": opensubtitles,
                "subdivx": subdivx,
                }

        hallados = []
        for scraper in scrapers:
            hallados += get_subs[scraper](palabras)
        editar_resultados(hallados)
        editar_settings("cambio_busqueda", "0")

    subs = leer_resultados()


    #Pantalla resultados
    numcols = num_cols()
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","3")

    #Definiendo colores de lineas
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
    linea_roja_ = colored(numcols*"-", 'red', attrs=['bold', 'dark'])
    linea_amarilla = colored(numcols*"=", 'yellow', attrs=['bold', 'dark'])

    titulo = "RESULTADOS"
    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo)
    print(linea_azul)

    for x in range(len(subs)):
        ID = colored("ID " + str(x), 'green', attrs=['bold', 'dark'])

        print(linea_amarilla)
        print(str(x) + ": " + ID + " -> " + subs[x][0])
        print(numcols * "-")
        print(fit_frase_centrada(numcols, subs[x][1]))
        print()
        by = [scraper for scraper in scrapers if scraper in subs[x][2]][0]
        by_color = colored(by, 'cyan', attrs=['bold'])
        print((numcols - len(by)) * " " + by_color)

    print(linea_amarilla)
    print("Página: 1 de 2 - 64 subs")
    print(linea_amarilla)
    print(linea_roja)
    #Nombre del video
    print(fit_frase_centrada(numcols, leer_settings("video")))
    print(linea_roja_)
    #ruta
    print(leer_settings("ruta_video"))
    print(linea_roja)
    i = menu(numcols)

    return i[1]

#quiero que no se reejecute la busqueda:
#en settings: cambio_busqueda = False or True
#si cambio ruta_video o video, cambio busqueda = True
#si cambio palabras, cambio_busqueda = True
#buscar solo si cambio_busqueda == True
#despues de buscar, agrega todo a db y cambio_busuqueda = False
#
#leer subs de db

#msj: vaya, no hubo subtítulos para esta búsqueda, prueba con otras palabras...
#Ningún subtítulo con el filtro indicado...

#================================== azul
#SUBTÍTULOS ENCONTRADOS
#================================== azul
#================================== amarillo
#0: ID 0 -> Titulo
#---------------------------------- amarillo
#Descripcion
#
#                           subdivx
#==================================
#0: ID 0 -> Titulo
#----------------------------------
#Descripcion
#
#                     opensubtitles
#================================== amarillo
#Pagina: 1 de 2 - 64 subs
#================================== amarillo
#================================== rojo
#Nombre de video 
#----------------------------------
#ruta:
#================================== rojo
#            MENU
#==================================
