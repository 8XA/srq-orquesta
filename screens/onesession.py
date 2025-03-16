#!/bin/env python 

import sys
from modules.admin_db import edit_settings
from os import system, execv

def one_session():
    edit_settings("active_instance", "0")

    #Restart SRQ
    system("stty echo")
    sys.stdout.flush()
    execv(sys.argv[0], sys.argv)

