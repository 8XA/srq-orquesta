#!/bin/env python 

import sys
from modules.columns_number import columns_number_func
from modules.admin_db import edit_settings
from modules.strings_fitting import phrase_fitting, centered_phrase_fitting
from termcolor import colored
from os import system, execv
from time import sleep

def one_session():
    cols_number = columns_number_func()

    red_line_ = colored(cols_number*"-", 'red', attrs=['bold', 'dark'])
    blue_line = colored(cols_number*"=", 'blue', attrs=['bold', 'dark'])
    green_enter = colored("Enter", 'green', attrs=['bold','dark'])
    green_n = colored("N", 'green', attrs=['bold','dark'])

    print(blue_line)
    message = "SRQ ORQUESTA está actualmente en ejecución o no se cerró correctamente. " + \
            "Tener más de una instancia abierta puede provocar un comportamiento inesperado."

    options = green_enter + ": Sí\n" + green_n + ": No\n"
    print(phrase_fitting(cols_number, message))
    print(red_line_)
    print(colored(centered_phrase_fitting(cols_number, "Desea forzar inicio?"), 'white', attrs=['bold']))
    print(red_line_)
    printable = options + blue_line + "\n: "
    i = input(printable)

    if i == "":
        edit_settings("active_instance", "0")
        
        print("\nForzando apertura...")
        sleep(1.5)

        #Restart SRQ
        system("stty echo")
        sys.stdout.flush()
        execv(sys.argv[0], sys.argv)

