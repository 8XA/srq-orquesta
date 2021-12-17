#!/bin/env python

import os, time
#from modules.columns_number import columns_number_func
from modules.viewer import visor

def update():
    rabs = '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/'
    ruta_backup = "/data/data/com.termux/files/usr/share/srq-orquesta/data_backup.db"

    os.system("clear")
    print("Verificando actualizaciones para SRQ ORQUESTA...\n")

    remoto = os.popen('cd '+ rabs + ' && git fetch origin master ' + \
            '&& git checkout remotes/origin/master').read()
    local = os.popen('cd ' + rabs + ' && git checkout master').read()
    
    #Verifica que haya alguna actualización en el repo
    if "commit" in local:
        print("Actualizando script...\n")
        os.system('rm -rf update')
        clonar = os.system('git clone --branch master --single-branch ' + \
                'https://github.com/8XA/srq-orquesta.git update')

        #Si la descarga se realizó con exito, hace la actualización
        if clonar == 0:
            os.system ("cp " + rabs + "data.db " + ruta_backup)
            os.system('rm -rf ' + rabs[:-1])
            os.system('mv update ' + rabs[:-1] + ' && clear')
            
            visor("ACTUALIZACIÓN COMPLETA", "update")
            input("Enter para salir...")

            return 'exit_srq'

    else:
        os.system("clear")
        print("Ya tienes la última versión de SRQ ORQUESTA. Nada para hacer...")
        time.sleep(1)
        os.system("clear")
        return 'videos'
