#!/bin/env python

from os import system, popen
from os.path import isfile
from sys import exit
from subprocess import Popen, PIPE

def verify():
    """
    Verify the installed dependencies and install those are missing.
    """

    #It runs only on termux
    if not isfile("/data/data/com.termux/files/usr/bin/termux-info"):
        return None
    
    #PKG verify and installation
    pkg_dependencies = [
            "wget",
            "iconv",
            "unrar",
            "p7zip",
            "readline",
            "file",
            "libxslt" # tpblite dependency
        ]

    #Gets the installed packages with apt
    
    command_apt = Popen("apt list --installed", shell=True, stdout=PIPE, stderr=PIPE)
    raw_apt = str(command_apt.stdout.read())
    split_apt = raw_apt.split("\\n")
    apt_list = [pkg[:pkg.index("/")] for pkg in split_apt if "/" in pkg]

    #List of the missing packages
    pkg_to_install = [to_install for to_install in pkg_dependencies if to_install not in apt_list]

    #Upgrading system packages
    if len(pkg_to_install) > 0:
        system("apt-get update")
        system("apt-get upgrade - y")

    #Install the missing packages
    for pkg in pkg_to_install:
        system("pkg install -y " + pkg)

    #PIP verify and installation
    pip_dependencies = [
            "tpblite",
            "termcolor",
            "chardet",
            "requests"
        ]

    #Backup of the pip freeze file
    freeze_route = '/data/data/com.termux/files/usr/share/srq-orquesta/pip_freeze.txt'
    if not isfile(freeze_route):
        system("pip freeze > " + freeze_route)

    #Gets the pip list from the backup pip file
    with open(freeze_route, "r") as file:
        raw_pip = file.readlines()
    pip_list = [pkg[:pkg.index("=")] for pkg in raw_pip]

    #List of the missing packages
    pip_to_install = [to_install for to_install in pip_dependencies if to_install not in pip_list]

    #Upgrade pip
    if len(pip_to_install) > 0:
        system("pip install --upgrade pip")
    #Install the missing packages
    for pkg in pip_to_install:
        system("pip install " + pkg)
    #Updates the pip file
    if len(pip_to_install) > 0:
        system("pip freeze > " + freeze_route)

    if len(pip_to_install) + len(pkg_to_install) > 0:
        system("clear")
        input("Dependencias actualizadas. Reinicia SRQ ORQUESTA. Enter: ")
        exit()
