#!/bin/env python

import readline
from modules.admin_db import read_simple_list, edit_simple_list

def refresh_history(table):
    
    history = read_simple_list(table)
    readline.clear_history()

    if len(history) > 20:
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
