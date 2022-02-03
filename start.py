#!/bin/env python


#try:
from modules.create_db import create_db
create_db()
from modules.admin_db import read_settings, edit_settings, restore_settings
restore_settings()

refresh = read_settings("refresh_screen") == 1

if not refresh:
    from modules.dependencies_verify import verify
    verify()

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

columns_num = columns_number_func()

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

    execute = None
    if not refresh: 
        #This is a loop function. It verifies the access to the storage.
        storage_verify()

        #Update search
        if read_settings("auto_update") == 1:
            execute = update()

    edit_settings("refresh_screen", "0") 

    #This piece of code runs all the interaction screens
    if read_settings("clean_history") == 1:
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
#    backups_route = '/data/data/com.termux/files/usr/share/srq-orquesta/'
#    system("rm " + backups_route + "pip_freeze.txt")
#    system("rm " + backups_route + "pip_list.txt")
#    system("rm " + backups_route + "srq-orquesta/data.db")
#    print("\n\n")
#    input("Ops! Ocurrió un error. Todas las configuraciones \
#            se han reiniciado. Inicia de nuevo.")
