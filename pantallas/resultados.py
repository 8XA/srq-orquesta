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
    #Resultados por pagina (rpp)
    rpp = 50
    os.system("clear")

    #Recuperar scrapers a utilizar
    scrapers = leer_settings("scrapers").split(",")
    scrapers.reverse()

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

    #Subtítulos con indices asignados
    subs = leer_resultados()
    subs = [list(subs[indice]) + [indice] for indice in range(len(subs))]

    #Actualizando info de pantalla en base de datos
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","3")

    filtro = ""
    while True:
        #Pantalla resultados
        numcols = num_cols()

        #Definiendo colores de lineas
        linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
        linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
        linea_roja_ = colored(numcols*"-", 'red', attrs=['bold', 'dark'])
        linea_amarilla = colored(numcols*"=", 'yellow', attrs=['bold', 'dark'])

        #Subs filtrados
        filtro = " ".join(filtro.split(",")).split(" ")
        subs_filtrados = [sub for sub in subs if len([palabra_filtro \
                for palabra_filtro in filtro if palabra_filtro.lower() \
                in (sub[0]+sub[1]).lower()]) == len(filtro)]

        titulo = "RESULTADOS"
        print(linea_azul)
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)

        for x in range(len(subs_filtrados)):
            ID = colored("ID " + str(subs_filtrados[x][3]), 'green', attrs=['bold', 'dark'])

            print(linea_amarilla)
            print(str(x) + ": " + ID + " -> " + subs_filtrados[x][0])
            print(numcols * "-")
            print(fit_frase_centrada(numcols, subs_filtrados[x][1]))
            print()
            by = [scraper for scraper in scrapers if scraper in subs_filtrados[x][2]][0]
            by_color = colored(by, 'cyan', attrs=['bold'])
            print((numcols - len(by)) * " " + by_color)

        print(linea_amarilla)
        print(linea_roja)
        #Nombre del video
        print(fit_frase_centrada(numcols, leer_settings("video")))
        print(linea_roja_)
        #ruta
        print(fit_frase_centrada(numcols, "Ruta:"))
        print(leer_settings("ruta_video"))
        print(linea_roja)
        i = menu(numcols, "Página: 1 de 2 - 64 subs")

        #Si es alguna pantalla del menu
        if i[0] == "menu":
            return i[1]

        #Si es enter
        elif i[1] == "":
            pass
        
        #Si retrocede pantalla
        elif i[1] == "..":
            pass

        #Si elige un subtitulo
#        elif es un numero valido:
#            pass

        else:
            filtro = i[1]


#de aqui tiene que editar en la base de datos el enlace que va a descargar
#y tiene que retornar un numero de pantalla, logicamente sera la pantalla de descarga
#
#Muestra los resultados de 50 en 50
#    avanzar entre paginas (enter)
#    retroceder entre paginas ("..")
#En esta pantalla se pueden filtrar subtitulos:
#    palabras filtro se separan por espacios y comas
#se puede elegir un numero de subtitulo 
#subs descargados se marcan


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
