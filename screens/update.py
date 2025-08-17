#!/bin/env python

import re
from time import sleep
from os import system, popen, execv
from subprocess import Popen, PIPE
from modules.viewer import viewer
from modules.admin_db import edit_settings, read_settings
import sys


def update():
    base_route = "/data/data/com.termux/files/usr/share/srq-orquesta/"
    absolute_route = f"{base_route}srq-orquesta/"
    updates_route = f"{base_route}update"
    data_backup_route = f"{base_route}data_backup.db"

    Popen("clear").wait()
    print("Verificando actualizaciones para SRQ ORQUESTA...\n")

    system(f"cd {absolute_route} && git fetch --tags")
    versions_list = sorted(
        [tag[:-1] for tag in popen(f"cd {absolute_route} && git tag").readlines()],
        key=lambda x: tuple(map(int, re.findall(r'\d+', x)))
    )
    current_version = popen(f"cd {absolute_route} && git describe --tags --exact-match").read()[:-1]

    if current_version in versions_list and versions_list[-1] != current_version:
        # Verifies if there is an update in the repositorie
        print("Actualizando script...\n")
        Popen(["rm", "-rf", updates_route], stdout=PIPE, stderr=PIPE)
        print()

        is_clonned = not system(
            f"git clone --branch {versions_list[-1]} --single-branch "
            f"https://github.com/8XA/srq-orquesta.git {updates_route}"
        )

        # If the download was successful, it executes the update
        if is_clonned:
            while read_settings('dimention_status') != 'stopped':
                edit_settings("dimention_status", "stop")
                sleep(0.5)

            Popen(
                ["cp", f"{absolute_route}data.db", data_backup_route],
                stdout=PIPE,
                stderr=PIPE
            ).wait()

            Popen(
                ["rm", "-rf", absolute_route[:-1]],
                stdout=PIPE,
                stderr=PIPE
            ).wait()

            Popen(
                ["mv", updates_route, absolute_route[:-1]],
                stdout=PIPE,
                stderr=PIPE
            ).wait()

            print()
            viewer("ACTUALIZACIÓN COMPLETA", "update")

            # Restart SRQ
            sys.stdout.flush()
            execv(sys.argv[0], sys.argv)

    else:
        Popen("clear").wait()
        print("Ya tienes la última versión de SRQ ORQUESTA. Nada para hacer...")
        sleep(1)
        Popen("clear").wait()

        return 'videos'
