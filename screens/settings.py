#!/bin/env python

from modules.columns_number import columns_number_func
from termcolor import colored, os
from modules.menu import menu
from modules.admin_db import read_settings, edit_settings
from modules.auto_start import *
from modules.strings_fitting import phrase_fitting, centered_phrase_fitting
from screens.update import *
from modules.create_db import create_db

def bold_blanco_centrado(n_cols, txt):
    return colored(centered_phrase_fitting(n_cols, txt), 'white', attrs=['bold'])


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


def settings():
    if read_settings("menu") != 5:
        edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","settings")
    numcols = columns_number_func()


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
    texto = centered_phrase_fitting(numcols, "Buscar actUalizaciones ahora")
    ind = texto.index("act")
    texto_1 = colored(texto[:ind + 3], 'white', attrs=['bold'])
    letra_u = colored("U", 'green', attrs=['bold', 'dark'])
    texto_2 = colored(texto[ind+4:], 'white', attrs=['bold'])

    print(texto_1 + letra_u + texto_2)
    print(linea_roja)

    
    #Verificar actualizaciones al iniciar
    updt = read_settings("auto_update")
    opcion(linea_azul_, linea_roja, numcols, \
            "Buscar actualizaciones al iniciar el programa", \
            [[updt, "1s", ": Sí"],[int("10"[updt]), "1n", ": No"]]
        )

    
    #Inicio automático
    inicio = read_settings("auto_start")
    opcion(linea_azul_, linea_roja, numcols, "Inicio automático al abrir Termux", \
            [[inicio, "2s", ": Sí"],[int("10"[inicio]), "2n", ": No"]]
        )


    #Ver una película y una carpeta por renglón
    oneline = read_settings("one_line")
    opcion(linea_azul_, linea_roja, numcols, "Un renglón para cada película/carpeta", \
            [[oneline, "3s", ": Sí"],[int("10"[oneline]), "3n", ": No"]])


    #Extensiones de video admitidas
    ext = read_settings("extensions")
    opcion(linea_azul_, linea_roja, numcols, "Extensiones de video admitidas", \
            [[ext.count("avi"), "4a", ": avi"], 
            [ext.count("mkv"), "4k", ": mkv"],
            [ext.count("mp4"), "4m", ": mp4"]]
        )


    #Recodificar a UTF-8
    recode = read_settings("recode")
    opcion(linea_azul_, linea_roja, numcols, "Recodificar subtítulos a UTF-8", \
            [[recode, "5s", ": Sí"],[int("10"[recode]), "5n", ": No"]])


    #Fuentes de búsqueda
    scrapers = read_settings("sub_getters")
    opcion(linea_azul_, linea_roja, numcols, "Fuentes de búsqueda", [\
            [scrapers.count("subdivx"), "6s", ": subdivx"],
            [scrapers.count("opensubtitles"), "6o", ": opensubtitles (experimental)"]
        ])


    #IDs descargables
    ids = read_settings("downloadable_ids")
    opcion(linea_azul_, linea_roja, numcols, "IDs descargables", [\
            [ids.count("page"), "7p", ": Página actual"],
            [ids.count("filtered"), "7f", ": Filtrados"],
            [ids.count("avaliables"), "7d", ": Disponibles"]
        ])


    #Reiniciar configuración
    texto = centered_phrase_fitting(numcols, "ReIniciar configuración")
    ind = texto.index("Re")
    texto_1 = colored(texto[:ind + 2], 'white', attrs=['bold'])
    letra_i = colored("I", 'green', attrs=['bold', 'dark'])
    texto_2 = colored(texto[ind+3:], 'white', attrs=['bold'])

    print(texto_1 + letra_i + texto_2)
    print(linea_roja)


    #Resultados por página
    rpp = str(read_settings("results_per_page"))
    texto = centered_phrase_fitting(numcols, "Resultados por página (#): " + rpp)
    ind = texto.index(":") - 2
    texto_1 = colored(texto[:ind], 'white', attrs=['bold'])
    numero = colored("#", 'green', attrs=['bold', 'dark'])
    texto_2 = colored(texto[ind + 1: ind + 4], 'white', attrs=['bold'])
    texto_3 = colored(rpp, 'grey', 'on_white', attrs=['bold'])
    print(texto_1 + numero + texto_2 + texto_3)
    print(linea_roja)

    
    i = menu(numcols, "Cambia una configuración")

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
        return read_settings("previous_menu")


    #Actualizaciones ahora
    elif i[1].lower() == "u":
        if update() == 100:
            return 'exit_srq'

    #Actualizaciones al iniciar
    elif i[1].lower() in bool_1:
        edit_settings("auto_update", str(bool_1.index(i[1])))
    
    #Inicio automático al abrir termux
    elif i[1].lower() in bool_2:
        edit_settings("auto_start", str(bool_2.index(i[1])))
        inicio_aut()

    #Un renglón por película/carpeta
    elif i[1].lower() in bool_3:
        edit_settings("one_line", str(bool_3.index(i[1])))

    #Recodificar a UTF-8
    elif i[1].lower() in bool_5:
        edit_settings("recode", str(bool_5.index(i[1])))

    #Extensiones de video admitidas
    elif i[1].lower() in ["4a", "4k", "4m"]:
        seleccion = i[1].lower()
        ext = read_settings("extensions").split(",")
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
            edit_settings("extensions", ",".join(ext_editada))

    #Fuentes de búsqueda
    elif i[1].lower() in ["6s", "6o"]:
        seleccion = i[1].lower()
        fuentes = read_settings("sub_getters").split(",")
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
            edit_settings("sub_getters", ",".join(fuentes_editada))

    #IDs descargables
    elif i[1].lower() in ["7p","7d","7f"]:
        seleccion = i[1].lower()
        
        op_selec = {
                "7p": "page",
                "7d": "avaliables",
                "7f": "filtered"
                }
        edit_settings("downloadable_ids", op_selec[seleccion])

    #Reiniciar configuración
    elif i[1].lower() == "i":
        os.system("rm '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db'")
        creadb()
        edit_settings("active_instance", "1")

    #Resultados por página
    elif i[1].isdigit():
        edit_settings("results_per_page", i[1])

    return 'settings'


