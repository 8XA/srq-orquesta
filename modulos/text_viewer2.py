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
    #Habilitar configuración de colores
    curses.start_color()

    #Dimensiones de pantalla
    numlines = curses.LINES
    numcols = curses.COLS
#    numlines = screen.getmaxyx()[0]
#    numcols = screen.getmaxyx()[1]

    titulo = arg[0]
    ruta = "/data/data/com.termux/files/usr/share/apocalipsis-orquesta/apocalipsis-orquesta/imprimibles/"

    #Funciones de orden para cada renglón
    orden = {
        ":w": fit_frase_centrada,
        ":f": fit_frase,
        ":l": (numcols - 2) * "-",
        ":L": (numcols - 2) * "="
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
                renglon_formateado = orden[formato[:2].lower()](numcols - 2, renglon[4:][:-1]).split("\n")
            elif (formato[:2].lower() == ":l") and (formato[3] == ":"):
                renglon_formateado = [orden[formato[:2]]]
            else:
                formato = ":sl:"
                renglon_formateado = [" "]

            hoja += [formato + renglon for renglon in renglon_formateado]

        #Divisor de documentos
        hoja += [":sl: ", ":Lr:" + (numcols - 2) * "="]

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
    #Título
    titulo = fit_frase_centrada(numcols, titulo).split("\n")
    win_titulo = curses.newwin(len(titulo) + 3, numcols, 0, 0)
    win_titulo.addstr(0,0, numcols * "=", curses.color_pair(3))
    for indice in range(len(titulo)):
        win_titulo.addstr(indice + 1,0, titulo[indice], curses.color_pair(1))
    win_titulo.addstr(len(titulo)+1,0, numcols * "=", curses.color_pair(3))
    win_titulo.refresh()
    
    #Scrollable
    win_manual = curses.newwin(numlines-(len(titulo) + 2), numcols, len(titulo) + 2, 0)
    #Habilitar flechas
    win_manual.keypad(True)


    #newwin(lineas, columnas, y, x)
#    win_manual = curses.newwin(5, numcols-2, 0, 0)
#    win_manual.addstr(2,1,"hola!")
#    win_manual.box()
#    win_manual.refresh()
#    input()
    #win_manual = newwin(numlines//2, numcols-2, 7, 0)

    #Impresión de pantalla
    posicion = 0
    while True:
        win_manual.clear()
        for linea in range(numlines - 7):
            if linea+posicion < len(hoja):
                formato = hoja[linea + posicion][:4]
                if formato in [":sl:", ":ff:", ":wc:"]:
                    win_manual.addstr(linea+1,1, hoja[linea+posicion][4:], curses.color_pair(par[formato[2]]))
                elif formato.lower() in [":wc:", ":la:", ":lr:", ":lb:"]:
                    win_manual.addstr(linea+1,1, hoja[linea+posicion][4:], curses.color_pair(par[formato[2]]) | curses.A_BOLD)

        win_manual.box()
        win_manual.refresh()

        i = win_manual.getch()
        if (i == curses.KEY_DOWN) and \
                ((numlines + posicion -1) < len(hoja)):
            posicion += 1
        elif (i == curses.KEY_UP) and (posicion > 0):
            posicion -= 1

    input()
    curses.endwin()
    os.system("stty sane && clear")

#    print(hoja)
#    input()
#    os.system("clear")
#    for x in hoja:
#        print(x)

