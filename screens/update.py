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

    branch_command = Popen(["git", "-C", base_route + "srq-orquesta", "status"], stdout=PIPE, stderr=PIPE)
    out, error = branch_command.communicate()
    branch = [branch for branch in ['master', 'develop'] if branch in str(out.splitlines()[0])][0]

    Popen("clear").wait()
    print("Verificando actualizaciones para SRQ ORQUESTA...\n")

    remote = popen('cd '+ absolute_route + ' && git fetch origin ' + branch + \
            ' && git checkout remotes/origin/' + branch).read()
    local = popen('cd ' + absolute_route + ' && git checkout ' + branch).read()
    
    # Verifies if there is an update in the repositorie
    if "commit" in local:
        print("Actualizando script...\n")
        Popen(["rm", "-rf", updates_route], stdout=PIPE, stderr=PIPE)
        clonar = system('git clone --branch ' + branch + ' --single-branch ' + \
                'https://github.com/8XA/srq-orquesta.git ' + updates_route)

        # If the download was successful, it executes the update
        if clonar == 0:
            while read_settings('dimention_status') != 'stopped':
                edit_settings("dimention_status", "stop")
                sleep(0.5)
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
