#!/bin/env python 

from sys import executable, argv
import sys #sys.stdout.flush
from subprocess import call
from modules.columns_number import columns_number_func
from modules.admin_db import edit_settings
from modules.strings_fitting import phrase_fitting, centered_phrase_fitting
from termcolor import colored
from time import sleep

def one_session():
    cols_number = columns_number_func()

    blue_line_ = colored(cols_number*"-", 'blue', attrs=['bold', 'dark'])
    blue_line = colored(cols_number*"=", 'blue', attrs=['bold', 'dark'])
    green_zero = colored("0", 'green', attrs=['bold','dark'])
    green_one = colored("1", 'green', attrs=['bold','dark'])

    print(blue_line)
    message = "SRQ ORQUESTA está actualmente en ejecución o no se cerró correctamente. " + \
            "Tener más de una instancia abierta puede provocar un comportamiento inesperado."

    options = green_one + ": Sí\n" + green_zero + ": No\n"
    print(phrase_fitting(cols_number, message))
    print(blue_line_)
    print(colored(centered_phrase_fitting(cols_number, "Desea forzar inicio?"), 'white', attrs=['bold']))
    print(blue_line_)
    printable = options + blue_line + "\n: "
    i = input(printable)

    if i.isdigit() and int(i) == 1:
        edit_settings("active_instance", "0")
        
        print("\nForzando apertura...")
        sleep(1.5)

        #Restart SRQ
        sys.stdout.flush()
        call([executable, argv[0]])

