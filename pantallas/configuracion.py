#!/bin/env python

from modulos.numcols import num_cols
from termcolor import colored
from modulos.menu import menu
from modulos.admindb import leer_settings, editar_settings
from modulos.fit_frases import *


def bold_blanco_centrado(n_cols, txt):
    return colored(fit_frase_centrada(n_cols, txt), 'white', attrs=['bold'])


#Primer número indica si está marcado o no
#[[1,"1s", ": Sí"], [0, "1n", ": No"]]
def opcion(linea_azul_, linea_roja, numcols, descripcion, opciones):

    print(bold_blanco_centrado(numcols, descripcion))
    print(linea_azul_)

    for opcion in opciones:
        #Marcada
        if opcion[0] == 1:
            print(colored(opcion[1], 'green', 'on_white', attrs=['bold', 'dark']) + \
                    colored(opcion[2], 'grey', 'on_white', attrs=['bold', 'dark']))
        #No marcada
        else:
            print(colored(opcion[1], 'green', attrs=['bold', 'dark']) + opcion[2])
    print(linea_roja)


def configuracion():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","4")
    numcols = num_cols()


    #Líneas
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
    inicio = leer_settings("ini_aut")
    opcion(linea_azul_, linea_roja, numcols, "Inicio automático", \
            [[inicio, "1s", ": Sí"],[int("10"[inicio]), "1n", ": No"]]
        )


    #Actualizar ahora
    texto = fit_frase_centrada(numcols, "Buscar actUalizaciones ahora")
    ind = texto.index("act")
    texto_1 = colored(texto[:ind + 3], 'white', attrs=['bold'])
    letra_u = colored("U", 'green', attrs=['bold', 'dark'])
    texto_2 = colored(texto[ind+4:], 'white', attrs=['bold'])

    print(texto_1 + letra_u + texto_2)
    print(linea_roja)

    
    #Verificar actualizaciones al iniciar
    updt = leer_settings("actualizar")
    opcion(linea_azul_, linea_roja, numcols, \
            "Buscar actualizaciones al iniciar el programa", \
            [[updt, "2s", ": Sí"],[int("10"[updt]), "2n", ": No"]]
        )

    
    #Extensiones de video admitidas
    ext = leer_settings("extensiones")
    opcion(linea_azul_, linea_roja, numcols, "Extensiones de video admitidas", \
            [[ext.count("avi"), "3a", ": avi"], 
            [ext.count("mkv"), "3k", ": mkv"],
            [ext.count("mp4"), "3m", ": mp4"]]
        )


    #Fuentes de búsqueda
    scrapers = leer_settings("scrapers")
    opcion(linea_azul_, linea_roja, numcols, "Fuentes de búsqueda", [\
            [scrapers.count("subdivx"), "4s", ": subdivx"],
            [scrapers.count("opensubtitles"), "4o", ": opensubtitles (experimental)"]
        ])


    #Resultados por página
    rpp = str(leer_settings("rpp"))
    texto = fit_frase_centrada(numcols, "Resultados por página (#): " + rpp)
    ind = texto.index(":") - 2
    texto_1 = colored(texto[:ind], 'white', attrs=['bold'])
    numero = colored("#", 'green', attrs=['bold', 'dark'])
    texto_2 = colored(texto[ind + 1: ind + 4], 'white', attrs=['bold'])
    texto_3 = colored(rpp, 'grey', 'on_white', attrs=['bold'])
    print(texto_1 + numero + texto_2 + texto_3)
    print(linea_roja)

    
    #IDs descargables
    ids = leer_settings("id_descargable")
    opcion(linea_azul_, linea_roja, numcols, "IDs descargables", [\
            [ids.count("pagina"), "5p", ": Página actual"],
            [ids.count("filtrados"), "5f", ": Filtrados"],
            [ids.count("disponibles"), "5d", ": Disponibles"]
        ])


    #Verificar actualizaciones al iniciar
    recode = leer_settings("recode")
    opcion(linea_azul_, linea_roja, numcols, "Recodificar subtítulos a UTF-8", \
            [[recode, "6s", ": Sí"],[int("10"[recode]), "6n", ": No"]])


    #Ver una película y una carpeta por renglón
    oneline = leer_settings("oneline")
    opcion(linea_azul_, linea_roja, numcols, "Un renglón para cada película/carpeta", \
            [[oneline, "6s", ": Sí"],[int("10"[oneline]), "6n", ": No"]])


    i = menu(numcols)

    #Si la accion ingresada corresponde al menú, abre la respectiva pantalla
    if i[0] == "menu":
        return i[1]
    return 0


