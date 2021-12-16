#!/bin/env python

import os
from subprocess import Popen, PIPE
from termcolor import colored
from modules.scrapers.subtitles.spanish.helpers.subdivx.download_url_getter import get_enlace
from modules.files_from_route import subs_en_ruta
from modules.admin_db import read_settings, edit_simple_list
from modules.strings_fitting import phrase_fitting, centered_phrase_fitting
from modules.columns_number import columns_number_func
from modules.admin_db import read_settings, edit_settings
from modules.menu import menu

def download():
    #Actualizando info de pantalla en base de datos
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","download")
    ruta_tmp = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/tmp"

    numcols = columns_number_func()
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
        link = read_settings("downloadable_sub_url")
        if "subdivx" in link:
            link = '--referer="' + link + '" "' + get_enlace(link) + '"'
        
        #Descarga en carpeta temporal
        os.system("rm -r " + ruta_tmp)
        os.system("mkdir " + ruta_tmp)
        os.system("wget -O " + ruta_tmp + "/sub " + link)
        print()

    except:
        print(linea_azul_)
        print(phrase_fitting(numcols, "El subtítulo no pudo ser" + \
                " descargado, verifica tu conexión e intenta de nuevo..."))
        print("\n")
        input("Enter para continuar...")
        return 'results'

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
                msj = centered_phrase_fitting(numcols, msj)
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

        nombre_final_sub = read_settings("selected_video_route") + \
                read_settings("selected_video_name")[:-3] + sub[1][-3:]

    except:
        print(linea_azul_)
        print(phrase_fitting(numcols, "El archivo presenta problemas," + \
                " intenta con otro subtítulo..."))
        print("\n")
        input("Enter para continuar...")
        return 'results'

    try:
        txt, codificacion = "Asignando...", ''
        if read_settings("recode") == 1:
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
        os.system(asigna[read_settings("recode")])

        print(".\n.\n.")
        print(bold_white("Listo!"))
        os.system("rm -r " + ruta_tmp)
        print(linea_azul)

        #Abre el video
        os.system("termux-open '" + read_settings("selected_video_route") + \
                read_settings("selected_video_name") + "'")
        selected_video = read_settings('selected_video_route') + \
                read_settings('selected_video_name')
        edit_simple_list('played_videos',selected_video,'add')

    except:
        print(linea_azul_)
        print(phrase_fitting(numcols, "Falló la codificación del " + \
                "subtítulo, intenta con otro..."))
        print("\n")
        input("Enter para continuar...")
        return 'results'

    i = menu(numcols)

    if i[0] == "menu":
        return i[1]
    else:
        return 'results'

