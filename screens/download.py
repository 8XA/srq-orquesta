#!/bin/env python

from time import sleep
from pathlib import Path
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
    numcols = columns_number_func()
    
    #Verificando que existe el video a subtitular
    video_route = read_settings("selected_video_route") + read_settings("selected_video_name")
    video_route = video_route.replace("\\'","\'")

    if not Path(video_route).is_file():
        Popen("clear").wait()
        print(phrase_fitting(numcols, "Selecciona un video primero..."))
        sleep(1.5)

        return 'videos'

    #Actualizando info de pantalla en base de datos
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","download")
    ruta_tmp = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/tmp"

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
        Popen(["rm", "-r", ruta_tmp]).wait()
        Popen(["mkdir", ruta_tmp]).wait()
        Popen("wget -O " + ruta_tmp + "/sub " + link, shell=True).wait()
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
        file_type = Popen(["file", ruta_tmp + "/sub"], stdout=PIPE, stderr=PIPE)
        file_type = str(file_type.stdout.read())
        is_rar = "rar" in file_type.lower()

        ext = "zip"
        if is_rar:
            ext = "rar"

        #Extrae subtitulos
        descomprimir = {
                "zip": ["7z", "x", "-y", ruta_tmp + "/sub", "-o", ruta_tmp + "/"],
                "rar": ["unrar", "x", "-y", ruta_tmp + "/sub", ruta_tmp + "/"]
                }
        Popen(descomprimir[ext]).wait()
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

        nombre_final_sub = video_route[:-3] + sub[1][-3:]

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
            txt = "Recodificado y asignando..."

            Popen(["mv", sub[0] + sub[1], sub[0] + "sub.srt"]).wait()
            codificacion = Popen(["chardetect", sub[0] + "sub.srt"], stdout=PIPE, stderr=PIPE)
            codificacion = str(codificacion.stdout.read())
            codificacion = codificacion.split(" ")[1]
            if "UTF-8" in codificacion:
                codificacion = "utf-8"
            sub[1] = "sub.srt"
        ruta_sub = sub[0] + sub[1]

        print(bold_white(txt))

        #Asigna el subtitulo
        if read_settings("recode") == 1:
            with open(ruta_sub, 'rb') as source_file:
                source_content = source_file.read()
            with open(ruta_sub, 'w+b') as final_file:
                final_file.write(source_content.decode(codificacion).encode('utf-8'))
        Popen(["mv", ruta_sub, nombre_final_sub]).wait()

        print(".\n.\n.")
        print(bold_white("Listo!"))
        Popen(["rm", "-r", ruta_tmp]).wait()
        print(linea_azul)

        #Abre el video
        edit_simple_list('played_videos', video_route, 'add')
        Popen(["xdg-open", video_route], stdout=PIPE, stderr=PIPE).wait()

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

