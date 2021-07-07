#!/bin/env python

import os
from termcolor import colored
from modulos.admindb import leer_settings
from modulos.numcols import num_cols
from modulos.menu import menu

def descarga():
    numcols = num_cols()
    
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_azul_ = colored(numcols*"-", 'blue', attrs=['bold', 'dark'])

    def bold_white(msj):
        return colored(msj, 'white', attrs=['bold'])

    titulo = "DESCARGA Y ASIGNACIÓN"
    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo)
    print(linea_azul)
    print(bold_white("Descargando..."))
    print("\n\n")

    print(linea_azul_)
    print(bold_white("Descomprimiendo..."))
    print("\n\n")

    titulo = "ELIGE TU SUBTÍTULO"
    print(linea_azul)
    print(((numcols-len(titulo))//2)*" " + titulo)
    print(linea_azul)
    print("\n\n")
   
    print(linea_azul_)
    print(bold_white("Recodificando y asignando..."))
    print("\n\n")
    
    print(linea_azul_)
    print(bold_white("Listo!"))
    print(linea_azul)

    i = menu(numcols)

    return i[1]


#si es subdivx, llama al modulo auxiliar de descarga para obtener el link real
#si no simplemente toma el enlace de la base de datos
#
#descarga con wget en una carpeta temporal
#
#identifica la ruta, nombre y tipo de comprimido
#
#utiliza unzip o un rar dependiendo del caso
#
#si aparece mas de un subtitulo, los muestra para elegir
#
#lo mueve a la carpeta del video con extension srt o ssa, segun sea el caso
#(aplica conversion si esta activado en settings)
#
#muestra listo
#input()
#retorna pantalla de resultados
#


#================================
#    DESCARGA Y ASIGNACIÓN
#================================
#Descargando...
#
#dfñlgkslñdfg
#ldñkgñldg
#dfagñl
#
#-------------------------------
#Descomprimiendo
#
#asdasdkjsanñdk
#
#
#================================
#    ELIGE TU SUBTÍTULO
#================================
#0: ALKSJDFNLKAJSDF
#1: laskdnfñlaksdf
#--------------------------------
#:
#
#
#--------------------------------
#Recodificando y asignando...
#
#
#asdnñkasfnñlkd
#
#Listo!
#================================
#            MENU






