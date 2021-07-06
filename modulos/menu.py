#!/bin/env python

#Menú general, apto para todas las pantallas
#Retorna la acción ingresada e indica si esta acción pertenece al menú o a la pantalla en turno

from modulos.admindb import leer_settings
from termcolor import colored

def menu(numcols):
    print(((numcols - 4)//2) *  " " + "MENÚ")
    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))

    #Marcado de palabra
    marcado = 'on_white'

    #Colorea iniciales
    iniciales = "PCAROYES"
    i = {}
    for x in range(len(iniciales)):
        if leer_settings("menu") == x:
            i[str(x)] = colored(iniciales[x], 'green', marcado, attrs=['bold', 'dark'])
        else:
            i[str(x)] = colored(iniciales[x], 'green', attrs=['bold', 'dark'])

    #Tramos sin iniciales ni barras, ordenados
    tramo = [["elículas"], ["arpeta"], ["P", "labras"], ["esultados"], 
            ["C", "nfiguración"], ["A", "uda"], ["Ac", "rca de"], ["alir"]]

    #Diccionarios de tramos coloreados y sus longitudes
    #Los separo en dos diccionarios que usarán las mismas claves porque colorear caracteres cambia su longitud
    t, T = {}, {}
    
    #Agrega a un diccionario los tramos coloreados, y al otro, la longitud de cada tramo
    for palabra in range(len(tramo)):
        for pieza in range(len(tramo[palabra])):
            T[str(palabra) + "_" + str(pieza)] = len(tramo[palabra][pieza])
            if palabra == leer_settings("menu"):
                t[str(palabra) + "_" + str(pieza)] = \
                        colored(tramo[palabra][pieza], 'red', marcado, attrs=['bold', 'dark'])
            else:
                t[str(palabra) + "_" + str(pieza)] = \
                        colored(tramo[palabra][pieza], 'yellow', attrs=['bold'])

    #Barra coloreada
    barra = colored(" | ", 'blue', attrs=['bold', 'dark'])

    #Lista con el orden de las piezas, utilizando las claves del diccionario
    orden_secciones = ["0","0_0","b","1","1_0","b","2_0","2","2_1","b","3","3_0",
            "b","4_0","4","4_1","b","5_0","5","5_1","b","6_0","6","6_1","b","7","7_0"]


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

    #Arma e imprime los renglones imprimibles
    for renglon in imprimir:
        print(((numcols - renglon[0])//2) * " " + "".join(renglon[1:]))

    
    ######################################################################


    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))

    #Acción del usuario
    i = input(": ")
    
    #Retorna una tupla con dos valores:
    #El primero indica si la opcion ingresada va dirigida al menu o a la pantalla
    #El segundo corresponde a la accion a ejecutar

    if i.upper() == "S":
        return ("menu", 100)
    elif i.upper() in iniciales and len(i) == 1:
        return ("menu", iniciales.index(i.upper()))
    else:
        return ("accion", i)

