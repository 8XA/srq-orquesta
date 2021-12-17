#!/bin/env python

from modules.create_db import create_db
create_db()
from modules.admin_db import read_settings, edit_settings, restore_settings
restore_settings()

import readline
from os import system
from screens.update import update
from screens.torrents import torrents
from screens.videos import videos
from screens.folder import folder
from screens.words import words
from screens.results import results
from screens.settings import settings
from screens.help import help_section
from screens.about import about
from screens.download import download
from screens.onesession import one_session
from modules.storage_verify import *
from modules.columns_number import columns_number_func
from modules.refresh_history import clean_history_tables
#from modules.strings_fitting import phrase_fitting

columns_num = columns_number_func()

#try:
if read_settings("active_instance") == 0:
    edit_settings("active_instance", "1")

    #All the user interaction screens:
    srq_orquesta = {
        'torrents': torrents,
        'videos': videos,
        'folder': folder,
        'words': words,
        'results': results,
        'settings': settings,
        'help_section': help_section,
        'about': about,
        'download': download,
        'update': update,
    }
#
#    srq_orquesta = {
#        0: torrents,
#        1: videos,
#        2: folder,
#        3: words,
#        4: results,
#        5: settings,
#        6: help_section,
#        7: about,
#        101: download,
#        102: update,
#

    #This is a loop function. It verifies the access to the storage.
    storage_verify()

    #Update search
    execute = 1
    if read_settings("auto_update") == 1:
        execute = update()

    #This piece of code runs all the interaction screens
    clean_history_tables()
    if execute != 'exit_srq':
        running = srq_orquesta['videos']()
        while running != 'exit_srq':
            readline.clear_history()
            running = srq_orquesta[running]()
    edit_settings("active_instance", "0") 

else:
    #This function avoid the double run of srq-orquesta
    one_session()

#except Exception as e:
#    print(e)
#    print()
#
#    system("rm '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db'")
#    print(phrase_fitting(columns_num, "Base de datos corrupta fue corregida. Reinicia Termux..."))
#    input()
