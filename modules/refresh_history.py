#!/bin/env python

import readline
from modules.admin_db import read_simple_list, \
        edit_simple_list, read_settings

def refresh_history(table):
    
    history = read_simple_list(table)
    readline.clear_history()

    if len(history) > read_settings("history_lenght") and len(history) != 0:
        history.pop(0)

    # Clear table
    edit_simple_list(table)

    # Update table
    for element in history:
        edit_simple_list(table, element, 'add')
        readline.add_history(element)

def clean_history_tables():
    for table in ['newtorrents_history',
                    'torrents_history',
                    'videos_history',
                    'folder_history',
                    'words_history',
                    'results_history']:
        edit_simple_list(table)
