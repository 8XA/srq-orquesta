#!/bin/env python

#Con esta pantalla puedes navegar entre las carpetas
#para seleccionar una nueva ruta de búsqueda de videos

from subprocess import Popen, PIPE
from pathlib import Path
from termcolor import colored
from modules.admin_db import edit_simple_list
from modules.refresh_history import refresh_history
from modules.admin_db import read_settings, edit_settings
from modules.columns_number import columns_number_func
from modules.menu import menu
from modules.strings_fitting import phrase_fitting, \
        centered_phrase_fitting, colored_centered_filter
from time import sleep

def folder():
    refresh_history('folder_history')
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","folder")

    ruta = read_settings("folder_route")
    cadena = [carpeta for carpeta in ruta.split("/") if carpeta != ""]

    filtros_str = " "
    while filtros_str != "":
        numcols = columns_number_func()
        linea_amarilla = colored(numcols*"=", 'yellow', attrs=['bold', 'dark'])
        linea_azul = colored(numcols*"=", 'blue', attrs=['bold', 'dark'])
        linea_roja = colored(numcols*"=", 'red', attrs=['bold', 'dark'])

        #List folders
        bash_route = ruta.replace("'", "\'")
        raw_content = Popen(["ls", "-L", bash_route], stdout=PIPE, stderr=PIPE)
        output, errors = raw_content.communicate()
        dirty_folders = output.decode('utf-8').splitlines()

        carpetas = [folder for folder in dirty_folders if \
                (Path(ruta + "/" + folder).is_dir() and folder != "")]
        carpetas = sorted(carpetas, key=str.casefold)


        #Printing title
        titulo = "SELECCIÓN DE CARPETA"
        print(linea_azul)
        print(((numcols-len(titulo))//2)*" " + titulo)
        print(linea_azul)
        print(linea_amarilla)

        filtros_str = " ".join(filtros_str.lower().split(","))
        filtros = filtros_str.split(" ")
        while '' in filtros:
            filtros.remove('')

        show_message = False
        for x in range(len(carpetas)):
            if len([filtro for filtro in filtros if filtro in \
                    carpetas[x].lower()]) == len(filtros):

                indice = colored(str(x), 'green', attrs=['bold', 'dark'])

                #Recorta el renglon si está activado "oneline" en settings
                if read_settings("one_line") == 1:
                    print(indice + ":",carpetas[x][:numcols - len(str(x)) - 2])
                else:
                    print(indice + ":",carpetas[x])
                show_message = True

        if len(carpetas) == 0:
            msj = "Fin de la ruta, no hay más carpetas adelante..."
        elif show_message == False:
            msj = "Prueba con otro filtro..."
        if show_message == False or len(carpetas) == 0:
            print("\n")
            print(phrase_fitting(numcols, msj))
            print("\n")

        print(numcols * "-")
        print(colored("nc", 'green', attrs=['bold', 'dark']) + ": Nueva Carpeta")
        print(colored("d#", 'green', attrs=['bold', 'dark']) + ": Eliminar Carpeta")
        print(linea_amarilla)

        #Ruta actual en franja roja
        print(linea_roja)
        print(colored(centered_phrase_fitting(numcols, "Ruta editable:"), 'white', attrs=['bold']))
        print(ruta)
        print(linea_roja)
        #Filtros
        print(colored(centered_phrase_fitting(numcols, "Filtros:"), 'white', attrs=['bold']))
        colored_filters = colored_centered_filter(numcols, \
                "  ".join(filtros))
        if len(filtros) > 0:
            print(colored_filters)
        print(linea_roja)

        i = menu(numcols, "Define la carpeta de búsqueda")

        #Ejecuta una acción dependiendo del comando ingresado
        if i[0] == "menu":
            return i[1]
        else:
            if i[1] == "":
                if read_settings("folder_route") != ruta:
                    edit_settings("videos_filter", "")
                    edit_settings("folder_route", ruta)
                return 'videos'

            elif (i[1][0].lower() == 'd') and (i[1][1:].isdigit()) and (len(carpetas) > int(i[1][1:])):
                
                folder = carpetas[int(i[1][1:])]
                message = phrase_fitting(numcols, "Está a punto de eliminar la carpeta '" + folder + "', así como su contenido. Esta acción requiere confirmación.")
                enter = colored("Enter", 'green', attrs=['bold', 'dark'])
                cancel = colored("C", 'green', attrs=['bold', 'dark'])

                enter_message = enter + ": Confirmar"
                cancel_message = cancel + ": Cancelar"

                Popen("clear").wait()
                print(linea_azul)
                print(message)
                print(numcols * "-")
                print(enter_message)
                print(cancel_message)
                print(linea_azul)

                delete = input(": ")
                if delete == "":
                    deletion = Popen(["rm", "-rf", ruta + "/" + folder], stderr=PIPE, stdout=PIPE)
                    error_deletion = str(deletion.stderr.read())

                    if error_deletion != "b''":
                        Popen("clear").wait()
                        print("Este directorio no puede ser eliminado...")
                        sleep(1)


            elif ((i[1].isdigit()) and (len(carpetas) > int(i[1]))) or i[1].lower() == 'nc':
                folder = ""
                new_folder_error = "b''"
                if i[1].lower() == 'nc':
                    while folder == "":
                        Popen("clear").wait()
                        folder = input("Nombre de carpeta: ")
                    new_folder = Popen(["mkdir", ruta + "/" + folder], stderr=PIPE, stdout=PIPE)
                    new_folder_error = str(new_folder.stderr.read())

                else:
                    folder = carpetas[int(i[1])]

                if i[1].lower() != 'nc' or new_folder_error == "b''":
                    cadena.append(folder)
                if new_folder_error != "b''":
                    Popen("clear").wait()
                    print("Nueva carpeta inválida...")
                    sleep(1)

                ruta = "/" + "/".join(cadena) + "/"
                filtros_str = " "

            elif i[1] == "..":
                if len(cadena) > 1:
                    cadena.pop()
                    filtros_str = " "
                ruta = "/" + "/".join(cadena) + "/"
            else:
                edit_simple_list('folder_history', i[1], 'add')
                filtros_str = i[1]
