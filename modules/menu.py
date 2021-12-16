#!/bin/env python

#Menú general, apto para todas las pantallas
#Retorna la acción ingresada e indica si esta acción pertenece al menú o a la pantalla en turno
#De manera opcional puedes pasar un segundo parámetro como mensaje imprimible debajo del menu

from time import sleep
import os
from modules.admin_db import read_settings, edit_settings, \
        edit_simple_list, edit_scraped_list
from termcolor import colored

def menu(*args):
    numcols = args[0]

    #Iniciales de retorno
    return_keys = {
        'T': 'torrents',
        'V': 'videos',
        'C': 'folder',
        'A': 'words',
        'R': 'results',
        'O': 'settings',
        'Y': 'help_section',
        'E': 'about',
        'S': 'exit_srq'
    }

    print(((numcols - 4)//2) *  " " + "MENÚ")
    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))

    #Marcado de palabra
    marcado = 'on_white'

    #Colorea iniciales
    iniciales = "TVCAROYES"
    i = {}
    for x in range(len(iniciales)):
        if read_settings("menu") == return_keys[iniciales[x]]:
            i[str(x)] = colored(iniciales[x], 'green', marcado, attrs=['bold', 'dark'])
        else:
            i[str(x)] = colored(iniciales[x], 'green', attrs=['bold', 'dark'])

    #Tramos sin iniciales ni barras, ordenados
    tramo = [["orrents"], ["ideos"], ["arpeta"], ["P", "labras"], ["esultados"], 
            ["C", "nfiguración"], ["A", "uda"], ["Ac", "rca de"], ["alir"]]

    #Diccionarios de tramos coloreados y sus longitudes
    #Los separo en dos diccionarios que usarán las mismas claves porque colorear caracteres cambia su longitud
    t, T = {}, {}
    
    #Agrega a un diccionario los tramos coloreados, y al otro, la longitud de cada tramo
    for palabra in range(len(tramo)):
        for pieza in range(len(tramo[palabra])):
            T[str(palabra) + "_" + str(pieza)] = len(tramo[palabra][pieza])
            if return_keys[iniciales[palabra]] == read_settings("menu"):
                t[str(palabra) + "_" + str(pieza)] = \
                        colored(tramo[palabra][pieza], 'red', marcado, attrs=['bold', 'dark'])
            else:
                t[str(palabra) + "_" + str(pieza)] = \
                        colored(tramo[palabra][pieza], 'yellow', attrs=['bold'])

    #Barra coloreada
    barra = colored(" | ", 'blue', attrs=['bold', 'dark'])

    #Lista con el orden de las piezas, utilizando las claves del diccionario
    orden_secciones = ["0","0_0","b","1","1_0","b","2","2_0","b","3_0","3","3_1","b","4","4_0",
            "b","5_0","5","5_1","b","6_0","6","6_1","b","7_0","7","7_1","b","8","8_0"]


    ######################################################################

    #La sección abajo ordena el menú en renglones y los centra, asegurando
    #que la falta de espacio en pantalla no divida las opciones del menu.

    ######################################################################
    
    #Determina los renglones
    #El primer valor de cada renglon corresponde a su longitud real
    longitud, renglon, imprimir = 0, [], []
    for pieza in orden_secciones:
        renglon.append(pieza)
        if "_" in pieza:
            longitud = longitud + T[pieza]
        elif pieza == "b":
            longitud = longitud + 3
        else:
            longitud = longitud + 1
        
        if longitud > numcols:
            if pieza == "b":
                renglon.insert(0,longitud)
                imprimir.append(renglon)
                renglon, longitud = [], 0
            else:
                rezaga = []
                while renglon[-1] != "b":
                    if "_" in renglon[-1]:
                        longitud -= T[renglon[-1]]
                    else:
                        longitud -= 1
                    rezaga.append(renglon.pop())
                rezaga.reverse()
                renglon.insert(0,longitud)
                imprimir.append(renglon)
                renglon, longitud = [], 0
                for subpieza in rezaga:
                    renglon.append(subpieza)
                    if "_" in subpieza:
                        longitud = longitud + T[subpieza]
                    elif subpieza == "b":
                        longitud = longitud + 3
                    else:
                        longitud = longitud + 1
    renglon.insert(0, longitud)
    imprimir.append(renglon)

    #Elimina barras de los extremos, en caso de existir
    for renglon in imprimir:
        if renglon[-1] == "b":
            renglon.pop()
            renglon[0] -= 3
        if renglon[1] == "b":
            renglon.pop(1)
            renglon[0] -= 3

    #Sustutuye valores de diccionario
    for renglon in imprimir:
        for pieza in range(len(renglon[1:])):
            if renglon[pieza+1] == "b":
                renglon[pieza+1] = barra
            elif "_" in renglon[pieza+1]:
                renglon[pieza+1] = t[renglon[pieza+1]]
            else:
                renglon[pieza+1] = i[renglon[pieza+1]]

    ##################################################
    
    #Agregado provisional de la 'N' en torrents, todo el módulo menú será rediseñado/refactorizado
    
    if read_settings("menu") == 'torrents':
        orrents = '\x1b[2m\x1b[1m\x1b[47m\x1b[31morre\x1b[0m' + \
        '\x1b[2m\x1b[1m\x1b[47m\x1b[32mN\x1b[0m' + \
        '\x1b[2m\x1b[1m\x1b[47m\x1b[31mts\x1b[0m'
    else:
        orrents = '\x1b[1m\x1b[33morre\x1b[0m' + \
        '\x1b[2m\x1b[1m\x1b[32mN\x1b[0m' + \
        '\x1b[1m\x1b[33mts\x1b[0m'

    imprimir[0][2] = orrents

    ##################################################

    #Arma e imprime los renglones imprimibles
    for renglon in imprimir:
        print(((numcols - renglon[0])//2) * " " + "".join(renglon[1:]))

    
    ######################################################################


    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))

    #Acción del usuario
    if len(args) > 1:
        print(args[1])
    i = input(": ")
    
    #Retorna una tupla con dos valores:
    #El primero indica si la opcion ingresada va dirigida al menu o a la pantalla
    #El segundo corresponde a la accion a ejecutar

    if i.upper() in return_keys:
        return ("menu", return_keys[i.upper()])

    #Abre el video
    elif i.upper() == "P":
        video_route = read_settings("selected_video_route") + \
                read_settings("selected_video_name")
        if os.path.isfile(video_route):
            edit_simple_list('played_videos', video_route, 'add')
            os.system("termux-open '" + video_route + "'")
        else:
            edit_simple_list('played_videos', video_route)
            os.system("clear")
            print("No hay un video seleccionado aún...")
            sleep(1)

        #Evita repetir descarga
        pantalla = 'results'
        if read_settings("menu") != 'download':
            pantalla = read_settings("menu")
        return ("menu", pantalla)

    elif i.upper() == "N":
        edit_scraped_list('torrents', 'clean')
        edit_settings('torrents_filter', '')
        return ("menu", 'torrents')
    
    return ("accion", i)

