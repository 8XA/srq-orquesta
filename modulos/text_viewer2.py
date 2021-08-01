#!/bin/env python

import os, curses
from modulos.fit_frases import *

def visor(*arg):
    #arg[0] = titulo
    #arg[1...10] = archivo1... archivo10
    ruta = "/data/data/com.termux/files/usr/share/apocalipsis-orquesta/apocalipsis-orquesta/imprimibles/"

#    :wc: white centrado
#    :Wc: bold, white centrado
#    :ff: fit frase
#    :la: linea - azul
#    :La: linea = azul
#    :lr: linea - roja
#    :Lr: linea = roja
#    :lb: linea - blanca

    #Funciones de orden para cada renglón
    orden = {
        ":w": fit_frase_centrada
        ":f": fit_frase
        ":l": numcols * "-"
        ":L": numcols * "="
            }

    if formato in [":wc:", ":Wc:", ":ff:"]:
        orden[formato[:2].lower()](numcols, msj)
    elif formato[:2].lower() == "l" and formato[3] == ":"
        orden[formato]

    #Lista de archivos
    #Cada archivo es una lista de renglones
    archivos_lista = []
    for archivo in arg[1:]:
        with open(ruta + archivo, "r") as archivo_texto:
            archivos_lista.append(archivo_texto.readlines())

    #Prueba imprimiendo primer archivo
    for renglon in archivos_lista[0]:
        print(renglon[4:])

    input()
#    
#    screen = curses.initscr()
#    #Muestra teclas ingresadas en pantalla
#    curses.noecho()
#    #Habilitar flechas
#    screen.keypad(True)
#    #Habilitar configuración de colores
#    curses.start_color()
#
#    #Dimensiones de pantalla
#    largo_pantalla = curses.LINES
#    ancho_pantalla = curses.COLS
#
#
#    #Base de impresion
#    screen.clear()
#    screen.addstr(y,x,valor)
#    screen.refresh()
#



    #Título
    #Ventana scroll con texto:
        #Flechas arriba y abajo navegan por el texto
        #Flechas izq y der, navegan saltando párrafos

    #Renglon admite:
#    :wc: white centrado
#    :Wc: bold, white centrado
#    :ff: fit frase
#    :la: linea - azul
#    :La: linea = azul
#    :lr: linea - roja
#    :Lr: linea = roja
#    :lb: linea - blanca
#
    #Finaliza curses y restaura pantalla
#    curses.endwin()
#    os.system("stty sane && clear")
#    
#    #Linea de final y leyenda de Enter para regresar
#
#    return largo_pantalla,ancho_pantalla

#abres archivo de texto
#lista split saltos de renglon
#a cada renglón se le aplica la función de acomodo definida al inicio, teniendo en cuenta el num de columnas
#separar cada renglon en caracteres para hacer un grid
#
#posicionar el grid dependiendo de las flechas, asignando a cada caracter el color que te toque dependiendo de
#el renglon al que pertenezca
