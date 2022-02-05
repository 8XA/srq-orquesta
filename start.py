#!/bin/env python

#try:
from modules.create_db import create_db
create_db()
from modules.admin_db import read_settings, edit_settings, restore_settings
restore_settings()

refreshed = read_settings("dimention_status") == "refreshing"

if not refreshed:
    edit_settings("torrents_page", "1")
    edit_settings("subs_page", "1")
    
    from modules.dependencies_verify import verify
    verify()

import readline
from time import sleep
from os import system
from threading import Thread
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
from modules.storage_verify import storage_verify
from modules.columns_number import columns_number_func
from modules.refresh_history import clean_history_tables
from modules.dimentions_monitor import dimentions_monitor

columns_num = columns_number_func()
system("stty echo")

#Dimentions monitoring
def dimentions_init():
    dimentions_thread = Thread(
            target=dimentions_monitor,
            daemon=True
        )
    dimentions_thread.start()

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

    if not refreshed: 
        #This is a loop function. It verifies the access to the storage.
        storage_verify()

        #Update search
        if read_settings("auto_update") == 1:
            update()

    if read_settings("clean_history") == 1:
        clean_history_tables()
    
    first_screen = 'videos'
    if refreshed:
        first_screen = read_settings('menu')

    #Starting the first screen
    edit_settings("dimention_status", "stopped")
    if first_screen not in ['update', 'help_section', 'download', 'about']:
        edit_settings("dimention_status", "running")
        dimentions_init()
    running = srq_orquesta[first_screen]()

    #This piece of code runs all the interaction screens
    while running != 'exit_srq':
        readline.clear_history()
        while read_settings("dimention_status") != "stopped":
            edit_settings("dimention_status", "stop")
            sleep(0.1)
        if running not in ['update', 'help_section', 'download', 'about']:
            edit_settings("dimention_status", "running")
            dimentions_init()
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
