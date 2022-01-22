#!/bin/env python

from modules.strings_fitting import phrase_fitting, centered_phrase_fitting
import os, curses

###################################################

def hoja_imprimible(columns_number, tupla_hojas):

    ruta = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/printables/spanish/"

    #Funciones de orden para cada renglón
    orden = {
        ":w": centered_phrase_fitting,
        ":f": phrase_fitting,
        ":l": (columns_number - 2) * "-",
        ":L": (columns_number - 2) * "="
            }

    #Lista de renglones de la hoja final
    hoja = []
    
    #Lista de archivos
    #Cada archivo es una lista de renglones
    for archivo in tupla_hojas:
        #Abre cada documento
        with open(ruta + archivo, "r") as archivo_texto:
            renglones = archivo_texto.readlines()
        
        #Rectifica cada renglon y lo agrega a 'hoja'
        for renglon in renglones:
            formato = renglon[:4]

            if formato in [":wc:", ":Wc:", ":ff:"]:
                renglon_formateado = orden[formato[:2].lower()](columns_number - 2, renglon[4:][:-1], tags=True).split("\n")
            elif (formato[:2].lower() == ":l") and (formato[3] == ":"):
                renglon_formateado = [orden[formato[:2]]]
            else:
                formato = ":sl:"
                renglon_formateado = [" "]

            hoja += [formato + renglon for renglon in renglon_formateado]

        #Divisor de documentos
        if len(tupla_hojas) > 1 and archivo != tupla_hojas[-1]:
            hoja += [":sl: ", ":Lr:" + (columns_number - 2) * "="]

    return hoja

###################################################

#    :wc: white centrado
#    :Wc: bold, white centrado
#    :ff: fit frase
#    :la: linea - azul
#    :La: linea = azul
#    :lr: linea - roja
#    :Lr: linea = roja
#    :lb: linea - blanca
#    :sl: salto de linea
#    <g>text<g> = texto verde
#    <b>text<b> = texto verde sobre blanco
#    <r>text<r> = texto verde sobre rojo
#    <a>text<a> = texto rojo sobre amarillo
#    <R>text<R> = texto gris sobre rojo
#    <B>text<B> = gris sobre blanco
#    <c>text<c> = texto cyan

#arg[0] = titulo
#arg[1...10] = archivo1... archivo10
def viewer(*arg):

    posicion = 0

    #Inicializa hoja con valor nulo
    hoja = None

    while hoja == None:
        titulo = arg[0]

        screen = curses.initscr()
        #Hace el cursor invisible
        curses.curs_set(0)
        #Habilitar configuración de colores
        curses.start_color()
        #Demanda Enter
        #curses.nocbreak()

        #Dimensiones de pantalla
        numlines = screen.getmaxyx()[0]
        columns_number = screen.getmaxyx()[1]

        #Hoja imprimible
        if hoja == None:
            hoja = hoja_imprimible(columns_number, arg[1:])

            #Coordenadas [y,x] para cada etiqueta a colorear
            tag_coordinates = {
                    "<g>": [],
                    "<b>": [],
                    "<r>": [],
                    "<a>": [],
                    "<R>": [],
                    "<c>": [],
                    "<B>": []
                }

            tags = {
                    "<g>": False,
                    "<b>": False,
                    "<r>": False,
                    "<a>": False,
                    "<R>": False,
                    "<c>": False,
                    "<B>": False
                }

            boolean_options = [True, False]
            for tag in tag_coordinates:
                for y in range(len(hoja)):
                    for x in range(len(hoja[y])):
                        possible_tag = hoja[y][x:x+3]
                        if len(possible_tag) >= 3 and possible_tag == tag:
                            tags[possible_tag] = boolean_options[boolean_options.index(tags[possible_tag]) -1]
                        if tags[tag]:
                            tag_coordinates[tag].append([y,x-3])

            all_coordinates = []
            for tag in tag_coordinates:
                all_coordinates += tag_coordinates[tag]


        #Colores por defecto (-1):
        curses.use_default_colors()

        #Colores personalizados
        curses.init_pair(1, -1, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        #Blue
        curses.init_pair(3, 19, -1)
        #green
        curses.init_pair(4, 34, -1)
        #green on white
        curses.init_pair(5, 34, 255)
        #green on red
        curses.init_pair(6, 34, 124)
        #red on yellow
        curses.init_pair(7, 124, 214)
        #grey on red
        curses.init_pair(8, 250, 124)
        #cyan
        curses.init_pair(9, 45, -1)
        #grey on white
        curses.init_pair(10, 233, 7)

        #Par de colores
        par = {
                "c": 1,
                "f": 1,
                "b": 1,
                "l": 1,
                "r": 2,
                "a": 3
                }

        tag_color_pair = {
                "<g>": 4,
                "<b>": 5,
                "<r>": 6,
                "<a>": 7,
                "<R>": 8,
                "<c>": 9,
                "<B>": 10
            }

        #Ventanas
        #Título
        titulo = centered_phrase_fitting(columns_number, titulo).split("\n")
        long_win_titulo = len(titulo) + 3
        
        #Solo si hay espacio para el titulo y para el mensaje de retorno:
        if numlines > long_win_titulo + 1:
            win_titulo = curses.newwin(long_win_titulo, columns_number, 0, 0)
            win_titulo.addstr(0,0, columns_number * "=", curses.color_pair(3) | curses.A_BOLD)
            for indice in range(len(titulo)):
                win_titulo.addstr(indice + 1,0, titulo[indice], curses.color_pair(1))
            win_titulo.addstr(len(titulo)+1,0, columns_number * "=", curses.color_pair(3) | curses.A_BOLD)
            win_titulo.refresh()

            #Mensaje de retorno
            win_retorno = curses.newwin(1, columns_number, numlines-1,0)
            win_retorno.addstr(0,0, "Enter: ")
            win_retorno.keypad(True)
            win_retorno.refresh()

        #Scrollable
        long_win_manual = numlines - long_win_titulo
        #Solo si cabe la ventana manual:
        if long_win_manual > 2:
            win_manual = curses.newwin(long_win_manual, columns_number, long_win_titulo -1, 0)

            #Impresión de pantalla
            long_lineas = numlines - long_win_titulo -2
            i = None
            #Con esta lista puedo controlar el string de ingreso.
            caracteres_i = []
            #Para un posible getch futuro:
#            caracteres_dic = {
#                    116: "t", 84: "t", 118: "v", 86: "v", 99: "c", 67: "c", 97: "a", 65: "a",
#                    114: "r", 82: "r", 111: "o", 79: "o", 121: "y", 89: "y", 101: "e", 69: "e",
#                    115: "s", 83: "s", 112: "p", 80: "p",
#                    }

            #Mientras no haya un resize de pantalla
            while i not in (-1, 410):
                win_manual.clear()
                for linea in range(long_lineas):
                    if linea+posicion < len(hoja):
                        formato = hoja[linea + posicion][:4]
                        if formato in [":sl:", ":ff:", ":wc:"]:

                            #Row printing with their setted colors
                            row = hoja[linea + posicion][4:]
                            indx_offset = 0
                            for indx in range(len(row) - (row.count("<g>") + row.count("<b>") + \
                                    row.count("<r>") + row.count("<a>") + row.count("<R>") + \
                                    row.count("<c>") + row.count("<B>")) * 3):

                                possible_tag = row[indx + indx_offset:indx + indx_offset + 3]
                                if len(row[indx + indx_offset:]) >= 3 and possible_tag in tags:
                                    indx_offset += 3
                                
                                if [linea + posicion, indx + indx_offset] in all_coordinates:
                                    color = [tag for tag in tag_coordinates if \
                                            [linea + posicion, indx + indx_offset] in tag_coordinates[tag]][0]
                                    win_manual.addch(linea + 1, indx + 1, row[indx + indx_offset], \
                                            curses.color_pair(tag_color_pair[color]) | curses.A_BOLD)

                                else:
                                    win_manual.addch(linea + 1, indx + 1, row[indx + indx_offset], \
                                            curses.color_pair(par[formato[2]]))
                        
                        elif formato.lower() in [":wc:", ":la:", ":lr:", ":lb:"]:
                            win_manual.addstr(linea+1,1, hoja[linea+posicion][4:], \
                                    curses.color_pair(par[formato[2]]) | curses.A_BOLD)

                win_manual.box()
                win_manual.refresh()
                
                if i == 10:
                    break
                elif i == 127:
                    caracteres_i = []
                    win_retorno.clear()
                    win_retorno.addstr(0,0, ": ")
                    win_retorno.refresh()
                i = win_retorno.getch()
                if i not in [258,259]:
                    caracteres_i.append(i)
                if (i == curses.KEY_DOWN) and \
                        ((long_win_manual + posicion -1) <= len(hoja)):
                    posicion += 1
                elif (i == curses.KEY_UP) and (posicion > 0):
                    posicion -= 1

        hoja = None
        curses.endwin()
        os.system("stty sane && clear")

        if i == 10:
            return type(i),i, caracteres_i
