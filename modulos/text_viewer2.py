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
    numlines = curses.LINES
    numcols = curses.COLS

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


    #Impresión de pantalla

    posicion = 0
    while True:
        screen.clear()
        for linea in range(numlines):
            formato = hoja[linea + posicion][:4]
            if formato in [":sl:", ":ff:", ":wc:"]:
                screen.addstr(linea,0, hoja[linea+posicion][4:], curses.color_pair(par[formato[2]]))
            elif formato.lower() in [":wc:", ":la:", ":lr:", ":lb:"]:
                screen.addstr(linea,0, hoja[linea+posicion][4:], curses.color_pair(par[formato[2]]) | curses.A_BOLD)

        screen.refresh()

        i = screen.getch()
        if i == curses.KEY_UP:
            posicion += 1
        elif i == curses.KEY_DOWN:
            posicion -= 1


    input()
    curses.endwin()
    os.system("stty sane && clear")

#    print(hoja)
#    input()
#    os.system("clear")
#    for x in hoja:
#        print(x)

