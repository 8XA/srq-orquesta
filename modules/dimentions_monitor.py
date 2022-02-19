#!/bin/env python

from modules.columns_number import columns_number_func
from modules.admin_db import edit_settings, read_settings
from os import execv
from time import sleep
import sys

def dimentions_monitor():
    """
    Restarts SRQ ORQUESTA when the size screen changes
    """

    current_size = columns_number_func(clean_screen=False)
    status = None
    while status == None:
        try:
            status = read_settings("dimention_status")
        except:
            sleep(0.1)

    while status != 'stopped':

        try:
            if read_settings("dimention_status") == "stop":
                edit_settings("dimention_status", "stopped")
                status = 'stopped'

            elif (read_settings("dimention_status") == "running" and \
                    current_size != columns_number_func(clean_screen=False) and \
                    read_settings('menu') not in ['update', 'help_section', 'download', 'about']) or \
                    read_settings("dimention_status") == 'refresh':

                edit_settings("dimention_status", "refreshing")
                edit_settings("active_instance", "0") 
                sys.stdout.flush()
                execv(sys.argv[0], sys.argv)
        except:
            pass

        sleep(0.05)
                    
