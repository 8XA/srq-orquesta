#!/bin/env python

from subprocess import Popen, PIPE
import os

#VERIFICA EL PERMISO DE ALMACENAMIENTO
def storage_verify():
    while True:
        comando = Popen(["ls","/sdcard"], stdout=PIPE, stderr=PIPE)
        verificador = comando.communicate()

        if comando.returncode != 0:
            os.system("termux-setup-storage")
        else:
            break
    return 0
