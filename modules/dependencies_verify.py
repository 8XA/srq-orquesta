#!/bin/env python

from os import system, popen
from os.path import isfile
from subprocess import Popen, PIPE, call
from sys import exit

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
            "ncurses-utils",
            "python-lxml", # Parser used for BeautifulSoup4
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
        system(f"pkg install -y { pkg }")

    #PIP verify and installation
    pip_dependencies = [
            "beautifulsoup4",
            "termcolor",
            "chardet",
            "requests",
            "cloudscraper", # Dependency for scrap-imdb
            "scrap-imdb"
        ]

    #Backup of the pip freeze file
    pip_freeze_route = '/data/data/com.termux/files/usr/share/srq-orquesta/pip_freeze.txt'
    pip_list_route = '/data/data/com.termux/files/usr/share/srq-orquesta/pip_list.txt'
    if not isfile(pip_freeze_route):
        system("pip freeze --user > " + pip_freeze_route)
    if not isfile(pip_list_route):
        system("pip list > " + pip_list_route)

    #Gets the pip list from the backup pip files 
    with open(pip_freeze_route, "r") as file:
        raw_pip_freeze = file.readlines()
    pip_freeze = [pkg[:pkg.index("=")] for pkg in raw_pip_freeze if "==" in pkg]

    with open(pip_list_route, "r") as file:
        raw_pip_list = file.readlines()
    pip_list = [pkg.split(" ")[0] for pkg in raw_pip_list[2:]]

    #Installed packages
    pip_packages = pip_freeze + pip_list

    #List of the missing packages
    pip_to_install = [to_install for to_install in pip_dependencies if to_install not in pip_packages]

    #Upgrade pip
    if len(pip_to_install) > 0:
        system("pkg up -y python-pip")
    #Install the missing packages
    for pkg in pip_to_install:
        system(f"pip install { pkg } --no-input")
    #Updates the pip file
    if len(pip_to_install) > 0:
        system(f"pip freeze --user > { pip_freeze_route }")
        system(f"pip list > { pip_list_route }")

    if len(pip_to_install) + len(pkg_to_install) > 0:
        system("clear")
        input("Dependencias actualizadas. Presiona Enter para reiniciar Termux: ")

        #Exiting SRQ
        exit()
