#!/bin/env python

#Selecciona las palabras de busqueda o ingresa una busqueda libre

from modulos.numcols import num_cols
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu
from modulos.fit_frases import *
from termcolor import colored

def palabras():
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","2")
    extensiones = leer_settings("extensiones").split(',')
    video = leer_settings("video")
    numcols = num_cols()

    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])

    titulo = "PALABRAS DE BÚSQUEDA"
    print(linea_azul)
    print(((numcols - len(titulo))//2) * " " + titulo)
    print(linea_azul)

    if leer_settings("video") == "":
        msj = "Aquí aparecerán palabras de búsqueda sugeridas " + \
                "cuando selecciones un video..."
        print("\n")
        print(fit_frase(numcols, msj))
        print("\n")

    #Lista de palabras
    else:
        palabras_del_titulo = [palabra for palabra in \
                " ".join(video.split(".")).split(" ") if (palabra != " " and \
                palabra != "" and palabra.lower() not in extensiones)]

        for x in range(len(palabras_del_titulo)):
            indice = colored(str(x), 'green', attrs=['bold', 'dark'])
            print(indice + ": " + palabras_del_titulo[x])

    print(linea_azul)
    print(linea_roja)
    print(colored(fit_frase_centrada(numcols, "Palabras a confirmar:"), \
            'white', attrs=['bold']))

    msj = "Aquí aparecerán las palabras de búsqueda que definas..."
    lista_palabras = leer_settings("palabras")
    if lista_palabras == "":
        print(fit_frase(numcols, msj))

    else:
        print(fit_frase_centrada(numcols, " ".join(lista_palabras.split(","))))
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
            if leer_settings("palabras") != "":
                return 3
            else:
                return 2

        #Si usa todas las palabras de la lista
        #Actualizar busqueda aunque ya se haya hecho con los mismos parámetros
        elif i[1].lower() == "u":
            editar_settings("cambio_busqueda","1")
            editar_settings("subs_descargados","")
            return 3

        elif (i[1].lower() == "t") and \
                (",".join(palabras_del_titulo) != leer_settings("palabras")):

            editar_settings("cambio_busqueda","1")
            editar_settings("subs_descargados","")
            editar_settings("palabras", ",".join(palabras_del_titulo))

            return 2

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
            if ",".join(palabras_candidatas) != leer_settings("palabras"):
                editar_settings("cambio_busqueda","1")
                editar_settings("subs_descargados","")
                editar_settings("palabras", ",".join(palabras_candidatas))

        #busqueda libre
        else:
            palabras_candidatas = [x for x in " ".join(i[1].split(",")).split(" ") if x != ""]

            if (",".join(palabras_candidatas) != leer_settings("palabras")) and \
                    len(palabras_candidatas) > 0:
                editar_settings("cambio_busqueda","1")
                editar_settings("subs_descargados","")
                editar_settings("palabras", ",".join(palabras_candidatas))
            else:
                pass

        return 2
