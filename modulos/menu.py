#!/bin/env python

#Menú general, apto para todas las pantallas
#Retorna la acción ingresada e indica si esta acción pertenece al menú o a la pantalla en turno

from modulos.admindb import leer_settings
from termcolor import colored

def menu(numcols):
    print(((numcols - 4)//2) *  " " + "MENÚ")
    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))

    #Colorea iniciales
    iniciales = "PCAROYES"
    i = {}
    for x in range(len(iniciales)):
        i[str(x)] = colored(iniciales[x], 'green', attrs=['bold', 'dark'])

    #Colorea las palabras
    tramo = [["elículas"], ["arpeta"], ["P", "labras"], ["esultados"], ["C", "nfiguración"], ["A", "uda"], ["Ac", "rca de"], ["alir"]]
    t = {}
    
    for palabra in range(len(tramo)):
        for pieza in range(len(tramo[palabra])):
            if palabra == leer_settings("menu"):
                t[str(palabra)+ "_" + str(pieza)] = colored(tramo[palabra][pieza], 'yellow', attrs=['bold', 'dark'])
            else:
                t[str(palabra)+ "_" + str(pieza)] = colored(tramo[palabra][pieza], 'yellow', attrs=['bold'])

    barra = colored(" | ", 'blue', attrs=['bold', 'dark'])

    #Ensambla las palabras con sus iniciales
    imprimir = i["0"] + t["0_0"] + barra + i["1"] + t["1_0"] + barra + t["2_0"] + i["2"] + t["2_1"] + barra + i["3"] + t["3_0"] + barra + t["4_0"] + i["4"] + t["4_1"] + barra + t["5_0"] + i["5"] + t["5_1"] + barra + t["6_0"] + i["6"] + t["6_1"] + barra + i["7"] + t["7_0"]


    orden_secciones = ["0","0_0","b","1","1_0","b","2_0","2","2_1","b","3","3_0","b","4_0","4","4_1","b","5_0","5","5_1","b","6_0","6","6_1","b","7","7_0"]






    print(imprimir)
    print(colored(numcols*"=", 'blue', attrs=['bold', 'dark']))

    i = input(": ")
    
    if i.upper() in iniciales and len(i) == 1:
        return ("menu", iniciales.index(i.upper()))
    else:
        return ("accion", i)

