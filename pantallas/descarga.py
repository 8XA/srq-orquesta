#!/bin/env python

import os
from subprocess import Popen, PIPE
from termcolor import colored
from modulos.scrapers.subs.auxiliares.subdivx.enlace_descarga import get_enlace
from modulos.archivos_en_ruta import subs_en_ruta
from modulos.admindb import leer_settings
from modulos.fit_frases import *
from modulos.numcols import num_cols
from modulos.admindb import leer_settings, editar_settings
from modulos.menu import menu

def descarga():
    #Actualizando info de pantalla en base de datos
    editar_settings("menu_anterior", str(leer_settings("menu")))
    editar_settings("menu","101")
    ruta_tmp = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/tmp"

    numcols = num_cols()
    linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
    linea_azul_ = colored(numcols*"-", 'blue', attrs=['bold', 'dark'])
    linea_roja_ = colored(numcols*"-", 'red', attrs=['bold', 'dark'])

    try:
        def bold_white(msj):
            return colored(msj, 'white', attrs=['bold'])

        titulo = "DESCARGA Y ASIGNACIÓN"
        print(linea_azul)
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)
        print(bold_white("Descargando..."))
        print("\n")

        #Recupera enlace de descarga
        link = leer_settings("link_descarga")
        if "subdivx" in link:
            link = '--referer="' + link + '" "' + get_enlace(link) + '"'
        
        #Descarga en carpeta temporal
        os.system("rm -r " + ruta_tmp)
        os.system("mkdir " + ruta_tmp)
        os.system("wget -O " + ruta_tmp + "/sub " + link)
        print()

    except:
        print(linea_azul_)
        print(fit_frase(numcols, "El subtítulo no pudo ser" + \
                " descargado, verifica tu conexión e intenta de nuevo..."))
        print("\n")
        input("Enter para continuar...")
        return 4

    try:
        print(linea_azul_)
        print(bold_white("Descomprimiendo..."))
        print("\n")

        #Determinando extension de archivo
        ext = "zip"
        if "rar" in os.popen("file " + ruta_tmp + "/sub").read().lower():
            ext = "rar"

        #Extrae subtitulos
        descomprimir = {
                "zip": "7z x -y " + ruta_tmp + "/sub -o" + ruta_tmp + "/",
                "rar": "unrar x -y " + ruta_tmp + "/sub " + ruta_tmp + "/"
                }
        os.system(descomprimir[ext])
        print("\n")
        
        subs = subs_en_ruta()

        if len(subs[1]) > 1:
            print(linea_azul)
            while True:
                msj = "*Este archivo contiene más de un subtítulo..."
                msj = fit_frase_centrada(numcols, msj)
                msj = msj.split("\n")
                for renglon in msj:
                    print(colored(renglon + (numcols-len(renglon)) * " ", \
                            'white', 'on_red', attrs=['bold', 'dark']))

                titulo = "ELIGE TU SUBTÍTULO"
                print(linea_azul)
                print(((numcols-len(titulo))//2)*" " + titulo)
                print(linea_azul)

                print(linea_roja_)
                for x in range(len(subs[1])):
                    id_sub = colored(str(x), 'green', attrs=['bold', 'dark'])
                    print(id_sub + ": " + subs[1][x])
                    print(linea_roja_)
                i = input(": ")
                if (len([x for x in i if x in "0123456789"]) == len(i)) and \
                        (i != "") and int(i) < len(subs[1]):

                    sub = [subs[0][int(i)], subs[1][int(i)]]
                    print()
                    print(linea_azul_)
                    break

                print()


                print(linea_azul)
        else:
            sub = [subs[0][0], subs[1][0]]
            print(linea_azul_)

        nombre_final_sub = leer_settings("ruta_video") + \
                leer_settings("video")[:-3] + sub[1][-3:]

    except:
        print(linea_azul_)
        print(fit_frase(numcols, "El archivo presenta problemas," + \
                " intenta con otro subtítulo..."))
        print("\n")
        input("Enter para continuar...")
        return 4

    try:
        txt, codificacion = "Asignando...", ''
        if leer_settings("recode") == 1:
            txt = "Recodificando y asignando..."

            os.system('mv "' + sub[0] + sub[1] + '" "' + sub[0] + 'sub.srt"')
            codificacion = os.popen('chardetect "' + sub[0] + 'sub.srt"').read().split(" ")[1]
            if "UTF-8" in codificacion:
                codificacion = "utf-8"
            sub[1] = "sub.srt"
        ruta_sub = sub[0] + sub[1]

        print(bold_white(txt))

        #Asigna el subtitulo
        asigna = {
                0: 'mv "' + ruta_sub + '" "' + nombre_final_sub + '"',
                1: 'iconv --from-code=' + codificacion + ' --to-code=utf-8 "' + \
                        ruta_sub + '" > "' + nombre_final_sub + '"'
                }
        os.system(asigna[leer_settings("recode")])

        print(".\n.\n.")
        print(bold_white("Listo!"))
        os.system("rm -r " + ruta_tmp)
        print(linea_azul)

        #Abre el video
        os.system("termux-open '" + leer_settings("ruta_video") + \
                leer_settings("video") + "'")

    except:
        print(linea_azul_)
        print(fit_frase(numcols, "Falló la codificación del " + \
                "subtítulo, intenta con otro..."))
        print("\n")
        input("Enter para continuar...")
        return 4

    i = menu(numcols)

    if i[0] == "menu":
        return i[1]
    else:
        return 4

