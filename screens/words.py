#!/bin/env python

#Selecciona las palabras de busqueda o ingresa una busqueda libre

from modules.refresh_history import refresh_history
from modules.columns_number import columns_number_func
from modules.admin_db import read_settings, edit_settings, edit_simple_list
from modules.menu import menu
from modules.strings_fitting import phrase_fitting, \
        centered_phrase_fitting, colored_centered_filter
from termcolor import colored

def words():
    refresh_history('words_history')
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","words")
    extensiones = read_settings("extensions").split(',')
    video = read_settings("selected_video_name")
    numcols = columns_number_func()

    linea_amarilla = colored(numcols*"=", 'yellow', attrs=['bold', 'dark'])
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])

    titulo = "PALABRAS DE BÚSQUEDA"
    print(linea_azul)
    print(((numcols - len(titulo))//2) * " " + titulo)
    print(linea_azul)
    print(linea_amarilla)

    if read_settings("selected_video_name") == "":
        msj = "Aquí aparecerán palabras de búsqueda sugeridas " + \
                "cuando selecciones un video..."
        print("\n")
        print(phrase_fitting(numcols, msj))
        print("\n")

    #Lista de palabras
    else:
        palabras_del_titulo = [palabra.replace("\\'","\'") for palabra in \
                " ".join(video.split(".")).split(" ") if (palabra != " " and \
                palabra != "" and palabra.lower() not in extensiones)]

        for x in range(len(palabras_del_titulo)):
            indice = colored(str(x), 'green', attrs=['bold', 'dark'])
            print(indice + ": " + palabras_del_titulo[x])

    print(linea_amarilla)
    print(linea_roja)
    print(colored(centered_phrase_fitting(numcols, "Palabras seleccionadas:"), \
            'white', attrs=['bold']))

    msj = "Aquí aparecerán las palabras de búsqueda que definas..."
    lista_palabras = read_settings("sub_words")
    if lista_palabras == "":
        print(phrase_fitting(numcols, msj))

    else:
        print(colored_centered_filter(numcols, " ".join(lista_palabras.split(","))))
    print(linea_roja)

    #Menú
    i = menu(numcols, "Define las palabras de búsqueda")

    #Si la accion ingresada corresponde al menú, abre la respectiva pantalla
    if i[0] == "menu":
        return i[1]

    #Ejecuta una acción dependiendo del comando ingresado
    else:
        #Si da enter
        if i[1] == "":
            if read_settings("sub_words") != "":
                return 'results'
            else:
                return 'words'

        #Si usa todas las palabras de la lista
        #Actualizar busqueda aunque ya se haya hecho con los mismos parámetros
        elif i[1].lower() == "u":
            edit_settings("sub_search_changed","1")
            return 'results'

        elif (i[1].lower() == "all") and \
                (",".join(palabras_del_titulo) != read_settings("sub_words")):

            edit_settings("sub_search_changed","1")
            edit_settings("sub_words", ",".join(palabras_del_titulo))

            return 'words'

        #Si selecciona palabras de la lista:
        elif all(
                [
                    #Solo contiene los caracteres admitidos
                    len([x for x in i[1] if x in "0123456789,-"]) == len(i[1]),

                    #Tiene por lo menos un número
                    len([x for x in i[1] if x in "0123456789"]) > 0,

                    #No hay puntos ni comas iniciales ni finales
                    i[1][0] not in ",-" and i[1][-1] not in ",-",
                    
                    #No hay dos símbolos seguidos
                    len([i[1][x] for x in range(len(i[1])-1) if \
                            (i[1][x] in "-," and i[1][x+1] in "-,")]) == 0,

                    #Ningún número es mayor al numero de palabras
                    len([num for num in [x for x in \
                            "-".join(i[1].split(",")).split("-") if (x != "" and \
                            len([digito for digito in x if digito in "0123456789"])\
                            == len(x))] if (int(num) >= len(palabras_del_titulo))]) == 0
                ]
            ):

            #La coma separa los rangos numéricos de los números aislados
            separacion = i[1].split(",")

            #Guion indica rango numérico
            palabras_candidatas = []
            for x in separacion:
                #Si es rango, agrega las palabras a la lista
                if "-" in x:
                    rango = x.split("-")
                    #Verifica que el orden del rango sea ascendente, y si no, lo corrige
                    if int(rango[0]) > int(rango[1]):
                        rango.reverse()
                    #Agrega las palabras
                    palabras_candidatas += [palabras_del_titulo[indice] for indice \
                            in [numero for numero in range(int(rango[0]), int(rango[1])+1)]]

                #Si es número, agrega su palabra a la lista
                else:
                    palabras_candidatas.append(palabras_del_titulo[int(x)])

            #Si todo esta correcto, guarda
            if ",".join(palabras_candidatas) != read_settings("sub_words"):
                edit_settings("sub_search_changed","1")
                edit_settings("sub_words", ",".join(palabras_candidatas))
                edit_simple_list('words_history', i[1], 'add')

        #busqueda libre
        else:
            palabras_candidatas = [x for x in " ".join(i[1].split(",")).split(" ") if x != ""]

            if (",".join(palabras_candidatas) != read_settings("sub_words")):
                edit_settings("sub_words", ",".join(palabras_candidatas))

                if len(palabras_candidatas) > 0:
                    edit_simple_list('words_history', i[1], 'add')
                    edit_settings("sub_search_changed","1")

        return 'words'
