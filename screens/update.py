#!/bin/env python

from time import sleep
from os import system, popen, execv
from subprocess import Popen, PIPE
from modules.viewer import viewer
from modules.admin_db import edit_settings, read_settings
import sys

def update():

    base_route = '/data/data/com.termux/files/usr/share/srq-orquesta/'
    absolute_route = base_route + 'srq-orquesta/'
    updates_route = base_route + 'update'
    data_backup_route = base_route + "data_backup.db"

    Popen("clear").wait()
    print("Verificando actualizaciones para SRQ ORQUESTA...\n")

    remote = popen('cd '+ absolute_route + ' && git fetch origin develop ' + \
            '&& git checkout remotes/origin/develop').read()
    local = popen('cd ' + absolute_route + ' && git checkout develop').read()
    
    # Verifies if there is an update in the repositorie
    if "commit" in local:
        print("Actualizando script...\n")
        Popen(["rm", "-rf", updates_route], stdout=PIPE, stderr=PIPE)
        clonar = system('git clone --branch develop --single-branch ' + \
                'https://github.com/8XA/srq-orquesta.git ' + updates_route)

        # If the download was successful, it executes the update
        if clonar == 0:
            Popen(["cp", absolute_route + "data.db", data_backup_route], stdout=PIPE, stderr=PIPE).wait()
            Popen(["rm", "-rf", absolute_route[:-1]], stdout=PIPE, stderr=PIPE).wait()
            Popen(["mv", updates_route, absolute_route[:-1]], stdout=PIPE, stderr=PIPE).wait()

            viewer("ACTUALIZACIÓN COMPLETA", "update")#

            #Restart SRQ
            sys.stdout.flush()
            execv(sys.argv[0], sys.argv)

    else:
        Popen("clear").wait()
        print("Ya tienes la última versión de SRQ ORQUESTA. Nada para hacer...")
        sleep(1)
        Popen("clear").wait()

        return 'videos'
