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

    filtro, pagina = "", 1
    while True:
        #Pantalla resultados
        numcols = num_cols()

        #Definiendo colores de lineas
        linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
        linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
        linea_roja_ = colored(numcols*"-", 'red', attrs=['bold', 'dark'])
        linea_amarilla = colored(numcols*"=", 'yellow', attrs=['bold', 'dark'])

        #Subs filtrados
        lista_filtro = " ".join(filtro.split(",")).split(" ")
        subs_filtrados = [sub for sub in subs if len([palabra_filtro \
                for palabra_filtro in lista_filtro if palabra_filtro.lower() \
                in (sub[0]+sub[1])+sub[2].lower()]) == len(lista_filtro)]
        subs_filtrados = [subs_filtrados[x]+[x] for x in range(len(subs_filtrados))]
        if len(subs_filtrados) == 0:
            pagina = 1

        #Total de paginas
        total_paginas = len(subs_filtrados)//rpp
        if total_paginas*rpp < len(subs_filtrados):
            total_paginas += 1

        #Subs de la página actual
        if pagina == 1:
            subs_pagina = subs_filtrados[rpp*pagina-1::-1]
        else:
            subs_pagina = subs_filtrados[(rpp*pagina)-1:(pagina-1)*rpp:-1]

        titulo = "RESULTADOS"
        print(linea_azul)
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)

        for x in range(len(subs_pagina)):
            ID = colored("ID " + str(subs_pagina[x][3]), 'green', attrs=['bold', 'dark'])

            print(linea_amarilla)
            print(str(subs_pagina[x][4]) + ": " + ID + " -> " + subs_pagina[x][0])
            print(numcols * "-")
            print(fit_frase_centrada(numcols, subs_pagina[x][1]))
            print()
            by = [scraper for scraper in scrapers if scraper in subs_pagina[x][2]][0]
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
        i = menu(numcols, "Página: " + str(pagina) + " de " + str(total_paginas)  + " - " + str(len(subs_filtrados))  + " subs")

        #Si es alguna pantalla del menu
        if i[0] == "menu":
            return i[1]

        #Si es enter
        elif i[1] == "":
            if pagina < total_paginas:
                pagina += 1
            else:
                pagina = 1
        
        #Si retrocede pantalla
        elif i[1] == "..":
            if total_paginas == 0:
                pagina = 1
            elif pagina == 1:
                pagina = total_paginas
            else:
                pagina -= 1

        #Si elige un subtitulo
#        elif es un numero valido:
#            pass

        else:
            filtro = i[1]


#de aqui tiene que editar en la base de datos el enlace que va a descargar
#y tiene que retornar un numero de pantalla, logicamente sera la pantalla de descarga
#
#Muestra los resultados de 50 en 50
#se puede elegir un numero de subtitulo 
#subs descargados se marcan

#msj: vaya, no hubo subtítulos para esta búsqueda, prueba con otras palabras...
#Ningún subtítulo con el filtro indicado...

