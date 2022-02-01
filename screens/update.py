#!/bin/env python

from time import sleep
from os import system, popen
from modules.viewer import viewer
from subprocess import call
from sys import executable, argv
import sys #sys.stdout.flush

def update():
    absolute_route = '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/'
    data_backup_route = "/data/data/com.termux/files/usr/share/srq-orquesta/data_backup.db"

    system("clear")
    print("Verificando actualizaciones para SRQ ORQUESTA...\n")

    remote = popen('cd '+ absolute_route + ' && git fetch origin develop ' + \
            '&& git checkout remotes/origin/develop').read()
    local = popen('cd ' + absolute_route + ' && git checkout develop').read()
    
    # Verifies if there is an update in the repositorie
    if "commit" in local:
        print("Actualizando script...\n")
        system('rm -rf update')
        clonar = system('git clone --branch develop --single-branch ' + \
                'https://github.com/8XA/srq-orquesta.git update')

        # If the download was successful, it executes the update
        if clonar == 0:
            system ("cp " + absolute_route + "data.db " + data_backup_route)
            system('rm -rf ' + absolute_route[:-1])
            system('mv update ' + absolute_route[:-1] + ' && clear')
            
            viewer("ACTUALIZACIÓN COMPLETA", "update")
            input("Enter para iniciar...")

            #Restart SRQ
            sys.stdout.flush()
            call([executable, argv[0]])

            return 'exit_srq'

    else:
        system("clear")
        print("Ya tienes la última versión de SRQ ORQUESTA. Nada para hacer...")
        sleep(1)
        system("clear")
        return 'videos'
