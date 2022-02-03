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
    status = read_settings("dimention_status")
    while status != 'stopped':

        if read_settings("dimention_status") == "stop":
            edit_settings("dimention_status", "stopped")
            status = 'stopped'

        elif read_settings("dimention_status") == "running" and \
                current_size != columns_number_func(clean_screen=False):

            edit_settings("dimention_status", "refreshing")
            edit_settings("active_instance", "0") 
            sys.stdout.flush()
            execv(sys.argv[0], sys.argv)

        elif read_settings("dimention_status") == "exception":
            current_size = columns_number_func(clean_screen=False)

        sleep(0.05)
                    
