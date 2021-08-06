#!/bin/env python

import os, curses
from modulos.fit_frases import *

#    :wc: white centrado
#    :Wc: bold, white centrado
#    :ff: fit frase
#    :la: linea - azul
#    :La: linea = azul
#    :lr: linea - roja
#    :Lr: linea = roja
#    :lb: linea - blanca
#    :sl: salto de linea

#arg[0] = titulo
#arg[1...10] = archivo1... archivo10
def visor(*arg):
    screen = curses.initscr()
    #Hace el cursor invisible
    curses.curs_set(0)
    #Muestra teclas ingresadas en pantalla
    curses.noecho()
    #Habilitar flechas
    screen.keypad(True)
    #Habilitar configuración de colores
    curses.start_color()

    #Dimensiones de pantalla
    #numlines = curses.LINES
    numlines = screen.getmaxyx()[0]
    numcols = screen.getmaxyx()[1]
    #numcols = curses.COLS

    titulo = arg[0]
    ruta = "/data/data/com.termux/files/usr/share/apocalipsis-orquesta/apocalipsis-orquesta/imprimibles/"

    #Funciones de orden para cada renglón
    orden = {
        ":w": fit_frase_centrada,
        ":f": fit_frase,
        ":l": numcols * "-",
        ":L": numcols * "=",
            }

    #Lista de renglones de la hoja final
    hoja = []
    
    #Lista de archivos
    #Cada archivo es una lista de renglones
    for archivo in arg[1:]:
        #Abre cada documento
        with open(ruta + archivo, "r") as archivo_texto:
            renglones = archivo_texto.readlines()
        
        #Rectifica cada renglon y lo agrega a 'hoja'
        for renglon in renglones:
            formato = renglon[:4]

            if formato in [":wc:", ":Wc:", ":ff:"]:
                renglon_formateado = orden[formato[:2].lower()](numcols, renglon[4:][:-1]).split("\n")
            elif (formato[:2].lower() == ":l") and (formato[3] == ":"):
                renglon_formateado = [orden[formato[:2]]]
            else:
                formato = ":sl:"
                renglon_formateado = [" "]

            hoja += [formato + renglon for renglon in renglon_formateado]

        #Divisor de documentos
        hoja += [":sl: ", ":Lr:" + numcols*"="]

    par = {
            "c": 1,
            "f": 1,
            "b": 1,
            "l": 1,
            "r": 2,
            "a": 3
            }

    #Colores por defecto (-1):
    curses.use_default_colors()

    #Colores personalizados
    curses.init_pair(1, -1, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)


    #Ventanas
    #Scrollable
    #newwin(lineas, columnas, y, x)
    window1 = curses.newwin(5, numcols-2, 0, 0)
    window = curses.newwin(numlines//2, numcols-2, 7, 0)
    window1.addstr(2,1,"hola!")
    window.addstr(2,1,"hola1!")
    window1.box()
    window.box()
    window.refresh()
    window1.refresh()
    input()
    #window = newwin(numlines//2, numcols-2, 7, 0)

    #Impresión de pantalla
#    posicion = 0
#    while True:
#        screen.clear()
#        for linea in range(numlines - 1):
#            if linea+posicion < len(hoja):
#                formato = hoja[linea + posicion][:4]
#                if formato in [":sl:", ":ff:", ":wc:"]:
#                    screen.addstr(linea,0, hoja[linea+posicion][4:], curses.color_pair(par[formato[2]]))
#                elif formato.lower() in [":wc:", ":la:", ":lr:", ":lb:"]:
#                    screen.addstr(linea,0, hoja[linea+posicion][4:], curses.color_pair(par[formato[2]]) | curses.A_BOLD)
#
#        screen.box()
#        screen.refresh()
#
#        i = screen.getch()
#        if (i == curses.KEY_DOWN) and \
#                ((numlines + posicion -1) < len(hoja)):
#            posicion += 1
#        elif (i == curses.KEY_UP) and (posicion > 0):
#            posicion -= 1

    input()
    curses.endwin()
    os.system("stty sane && clear")

#    print(hoja)
#    input()
#    os.system("clear")
#    for x in hoja:
#        print(x)

