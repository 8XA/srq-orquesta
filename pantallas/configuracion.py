#!/bin/env python

from modulos.numcols import num_cols
from termcolor import colored
from modulos.menu import menu
from modulos.admindb import leer_settings, editar_settings
from modulos.inicio_aut import *
from modulos.fit_frases import *
from pantallas.actualizar import *

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
    if leer_settings("menu") != 4:
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
            [[updt, "1s", ": Sí"],[int("10"[updt]), "1n", ": No"]]
        )

    
    #Inicio automático
    inicio = leer_settings("ini_aut")
    opcion(linea_azul_, linea_roja, numcols, "Inicio automático al abrir Termux", \
            [[inicio, "2s", ": Sí"],[int("10"[inicio]), "2n", ": No"]]
        )


    #Ver una película y una carpeta por renglón
    oneline = leer_settings("oneline")
    opcion(linea_azul_, linea_roja, numcols, "Un renglón para cada película/carpeta", \
            [[oneline, "3s", ": Sí"],[int("10"[oneline]), "3n", ": No"]])


    #Extensiones de video admitidas
    ext = leer_settings("extensiones")
    opcion(linea_azul_, linea_roja, numcols, "Extensiones de video admitidas", \
            [[ext.count("avi"), "4a", ": avi"], 
            [ext.count("mkv"), "4k", ": mkv"],
            [ext.count("mp4"), "4m", ": mp4"]]
        )


    #Recodificar a UTF-8
    recode = leer_settings("recode")
    opcion(linea_azul_, linea_roja, numcols, "Recodificar subtítulos a UTF-8", \
            [[recode, "5s", ": Sí"],[int("10"[recode]), "5n", ": No"]])


    #Fuentes de búsqueda
    scrapers = leer_settings("scrapers")
    opcion(linea_azul_, linea_roja, numcols, "Fuentes de búsqueda", [\
            [scrapers.count("subdivx"), "6s", ": subdivx"],
            [scrapers.count("opensubtitles"), "6o", ": opensubtitles (experimental)"]
        ])


    #IDs descargables
    ids = leer_settings("id_descargable")
    opcion(linea_azul_, linea_roja, numcols, "IDs descargables", [\
            [ids.count("pagina"), "7p", ": Página actual"],
            [ids.count("filtrados"), "7f", ": Filtrados"],
            [ids.count("disponibles"), "7d", ": Disponibles"]
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

    
    i = menu(numcols)

    #Auxiliares para valores booleanos
    bool_1 = ["1n", "1s"]
    bool_2 = ["2n", "2s"]
    bool_3 = ["3n", "3s"]
    bool_5 = ["5n", "5s"]

    #Si la accion ingresada corresponde al menú, abre la respectiva pantalla
    if i[0] == "menu":
        return i[1]
    
    #Acciones:
    elif i[1] == "":
        return leer_settings("menu_anterior")


    #Actualizaciones ahora
    elif i[1].lower() == "u":
        if actualizar() == 100:
            return 100

    #Actualizaciones al iniciar
    elif i[1].lower() in bool_1:
        editar_settings("actualizar", str(bool_1.index(i[1])))
    
    #Inicio automático al abrir termux
    elif i[1].lower() in bool_2:
        editar_settings("ini_aut", str(bool_2.index(i[1])))
        inicio_aut()

    #Un renglón por película/carpeta
    elif i[1].lower() in bool_3:
        editar_settings("oneline", str(bool_3.index(i[1])))

    #Recodificar a UTF-8
    elif i[1].lower() in bool_5:
        editar_settings("recode", str(bool_5.index(i[1])))

    #Extensiones de video admitidas
    elif i[1].lower() in ["4a", "4k", "4m"]:
        seleccion = i[1].lower()
        ext = leer_settings("extensiones").split(",")
        ext.sort()
        ext_editada = [x for x in ext]

        #Opcion extension
        op_ext = {"4a": "avi", "4k": "mkv", "4m": "mp4"}

        if op_ext[seleccion] not in ext_editada:
            ext_editada.append(op_ext[seleccion])
        elif len(ext_editada) > 1:
            ext_editada.remove(op_ext[seleccion])
        ext_editada.sort()

        if ext_editada != ext:
            editar_settings("extensiones", ",".join(ext_editada))

    #Fuentes de búsqueda
    elif i[1].lower() in ["6s", "6o"]:
        seleccion = i[1].lower()
        fuentes = leer_settings("scrapers").split(",")
        fuentes.sort()
        fuentes_editada = [x for x in fuentes]

        #Opcion extension
        op_fuentes = {"6s": "subdivx", "6o": "opensubtitles"}

        if op_fuentes[seleccion] not in fuentes_editada:
            fuentes_editada.append(op_fuentes[seleccion])
        elif len(fuentes_editada) > 1:
            fuentes_editada.remove(op_fuentes[seleccion])
        fuentes_editada.sort()

        if fuentes_editada != fuentes:
            editar_settings("scrapers", ",".join(fuentes_editada))

    #IDs descargables
    elif i[1].lower() in ["7p","7d","7f"]:
        seleccion = i[1].lower()
        
        op_selec = {
                "7p": "pagina",
                "7d": "disponibles",
                "7f": "filtrados"
                }
        editar_settings("id_descargable", op_selec[seleccion])

    #Resultados por página
    elif i[1].isdigit():
        editar_settings("rpp", i[1])

    else:
        return 5

    return 4


