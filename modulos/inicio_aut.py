#!/bin/env python

from modulos.admindb import leer_settings

#Cambia el bashrc para iniciar o no,
#el script de forma automática
def inicio_aut():
    ini = leer_settings("ini_aut")
    ruta_bash = '/data/data/com.termux/files/usr/etc/bash.bashrc'
    comando = 'exec python /data/data/com.termux/files/usr/share' + \
            '/srq-orquesta/srq-orquesta/start.py\n'

    with open(ruta_bash, "r") as bash:
        conf = bash.readlines()
    
    if (conf[0] == comando) and (ini == 0):
        conf.pop(0)
    elif (conf[0] != comando) and (ini == 1):
        conf.insert(0, comando)

    with open(ruta_bash, "w") as bash:
        bash.write("".join(conf))

    #Solo indica que el módulo finalizo
    return 0



