#!/bin/env python

from modulos.numcols import num_cols
from termcolor import colored
from modulos.menu import menu
from modulos.admindb import leer_settings, editar_settings
from modulos.fit_frases import *

def bold_blanco_centrado(n_cols, txt):
    return colored(fit_frase_centrada(n_cols, txt), 'white', attrs=['bold'])


def configuracion():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","4")
    numcols = num_cols()

    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])
    linea_azul_ = colored(numcols*"-", 'blue', attrs=['bold', 'dark'])
    linea_roja_ = colored(numcols*"-", 'red', attrs=['bold', 'dark'])

    titulo = "CONFIGURACIÓN"
    print(linea_azul)
    print(((numcols - len(titulo))//2) * " " + titulo)
    print(linea_azul)
    print(linea_roja)

    #Inicio automático
    print(bold_blanco_centrado(numcols, "Inicio automático"))
    print(linea_azul_)
    print(fit_frase_centrada(numcols, "Si    No"))
    print(linea_roja)

    #Verificar actualizaciones al iniciar
    print(bold_blanco_centrado(numcols, "Buscar actualizaciones al iniciar el programa"))
    print(linea_azul_)
    print(fit_frase_centrada(numcols, "Si    No"))
    print(linea_roja)

    #Verificar actualizaciones al iniciar
    print(bold_blanco_centrado(numcols, "Buscar actualizaciones ahora"))
    print(linea_azul_)
    print(fit_frase_centrada(numcols, "Si    No"))
    print(linea_roja)

    #Verificar actualizaciones al iniciar
    print(bold_blanco_centrado(numcols, "Extensiones de video admitidas"))
    print(linea_azul_)
    print(fit_frase_centrada(numcols, "mp4      mkv     avi"))
    print(linea_roja)

    #Fuentes de búsqueda
    print(fit_frase_centrada(numcols, "Fuentes de búsqueda"))
    print(linea_azul_)
    print(fit_frase_centrada(numcols, "subdivx      opensubtitles"))
    print(linea_roja)
    i = menu(numcols)

    #Si la accion ingresada corresponde al menú, abre la respectiva pantalla
    if i[0] == "menu":
        return i[1]
    return 0

#=========================
#      CONFIGURACION
#=========================
#Inicio automatico:
#    Si  No
#-------------------------
#Buscar actualizaciones al iniciar el programa:
#    Si  No
#-------------------------
#Buscar actualizaciones ahora
#-------------------------
#Extensiones de video admitidas
#-------------------------
#Fuentes de búsqueda
#    subdivx     opensubtitles (experimental)
#-------------------------
#Resultados por pagina: 
#-------------------------
#IDs descargables:
#    Página actual
#    Filtrados
#    Disponibles
#-------------------------
#Recodificar subtítulos a UTF-8
#    Si  No
#-------------------------
#Ver una pelicula y una carpeta por renglón
#    Si  No
#-------------------------
#Menu



#linea punteada con iguales roja
#descripcion de opcion, bold y centrada
#linea punteada con guiones azul
#opciones coloreadas:
#    param 1: numcols
#    param 2: description
#    param 3: lista de opciones, cada opcion es una sublista:
#        sublista: 1er elemento: switch marcado
#        los demas elementos son los componentes de la opcion, el que tenga _ es el verde

def configurar(columnas, texto, opciones):
    print(colored(columnas * "=", 'red', attrs=['bold', 'dark']))
    print(colored(fit_frase_centrada(columnas, texto), 'white', attrs=['bold']))
    print(colored(columnas * "-", 'blue', attrs=['bold', 'dark']))

#    opciones_long = len([opciones[opcion][pieza][c] for opcion in range(len(opciones)) \
#            for pieza in range(1,len(opciones[opcion])) for c in \
#            range(len(opciones[opcion][pieza])) if opciones[opcion][pieza][c] != "_"]) + \
#            (len(opciones) - 1) * 4

    #Cantidad de caracteres que seran centrados, considerando una separacion
    #de 4 espacios entre cada opción
    opciones_long = sum([sum(elemento) for elemento in[[len([c for c in pieza \
            if c != "_"]) for pieza in opcion[1:]] for opcion in opciones]]) + \
            (len(opciones) - 1) * 4




#[[1, '_1', ':Sí'], [0, '_2', ':No']]
