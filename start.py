#!/bin/env python

try:
    from modules.create_db import create_db
    create_db()
    from modules.admin_db import read_settings, edit_settings, restore_settings
    restore_settings()
    from multiprocessing import current_process
    from subprocess import Popen, PIPE
    from modules.allow_external_apps import allow_external_apps

    allow_external_apps()
    refreshed = read_settings("dimention_status") == "refreshing"

    if not refreshed:
        edit_settings("torrents_page", "1")
        edit_settings("subs_page", "1")
        
        from modules.dependencies_verify import verify
        verify()
    else:
        #Delete the old processes
        pid = str(current_process().pid)

        pids_command = Popen(["pidof","python"], stdout=PIPE, stderr=PIPE)
        raw_pids = str(pids_command.stdout.read())
        cleaned_raw_pids = raw_pids[2:-3]
        pids_list = cleaned_raw_pids.split(" ")
        pids_list.remove(pid)
        
        Popen(["kill", "-9"] + pids_list, stdout=PIPE, stderr=PIPE).wait()

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
    edit_settings("dimention_status", "running")
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
        running = srq_orquesta[first_screen]()

        #This piece of code runs all the interaction screens
        while running != 'exit_srq':
            readline.clear_history()
            running = srq_orquesta[running]()
        edit_settings("active_instance", "0") 

    else:
        #This function avoid the double run of srq-orquesta
        one_session()

except Exception as e:
    print(e)
    print()

    base_route = '/data/data/com.termux/files/usr/share/srq-orquesta/'
    branch_command = Popen(["git", "-C", base_route + "srq-orquesta", "status"], stdout=PIPE, stderr=PIPE)
    out, error = branch_command.communicate()
    branch = [branch for branch in ['master', 'develop'] if branch in str(out.splitlines()[0])][0]

    if branch == 'master':
        base_route = '/data/data/com.termux/files/usr/share/srq-orquesta/'
        system("rm " + base_route + "pip_freeze.txt")
        system("rm " + base_route + "pip_list.txt")
        system("rm " + base_route + "srq-orquesta/data.db")
        print("\n\n")
        input("Ops! Ocurrió un error. Todas las configuraciones \
                se han reiniciado. Inicia de nuevo.")
