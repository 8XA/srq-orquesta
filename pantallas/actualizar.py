#!/bin/env python

import os, time
from modulos.numcols import num_cols
from modulos.text_viewer import visor

def actualizar():
    rabs = '/data/data/com.termux/files/usr/share/sub4time/sub4time/'
    ruta_backup = "/data/data/com.termux/files/usr/share/sub4time/data_backup.db"
    numcols = num_cols()
    
    print("Verificando actualizaciones para SUB4TIME...\n")

    remoto = os.popen('cd '+ rabs + ' && git fetch origin master ' + \
            '&& git checkout remotes/origin/master').read()
    local = os.popen('cd ' + rabs + ' && git checkout master').read()
    
    #Verifica que haya alguna actualización en el repo
    if "commit" in local:
        print("Actualizando script...\n")
        os.system('rm -rf update')
        clonar = os.system('git clone --branch master --single-branch ' + \
                'https://github.com/8XA/sub4time.git update')

        #Si la descarga se realizó con exito, hace la actualización
        if clonar == 0:
            os.system ("cp " + rabs + "data.db " + ruta_backup)
            os.system('rm -rf ' + rabs[:-1])
            os.system('mv update ' + rabs[:-1] + ' && clear')
            
            visor("ACTUALIZACIÓN COMPLETA", "actualizacion")
            input("Enter para salir...")

            return 100

    else:
        os.system("clear")
        print("Ya tienes la última versión de Sub4Time. Nada para hacer...")
        time.sleep(1)
        os.system("clear")
        return 0
