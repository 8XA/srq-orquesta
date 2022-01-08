#!/bin/env python

#This module has the functions to read and edit the database and its backup

from sqlite3 import connect
from os.path import isfile
from os import system
from os.path import isfile

data_route = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db"
data_backup_route = "/data/data/com.termux/files/usr/share/srq-orquesta/data_backup.db"

######################################################################

def read_settings(
        column:str='*',
        db:str='data_route'
    ):

    """DESCRIPTION:
        - This module allows you to read the settings table.

    PARAMETERS:
        - column: This is the column that contains the wished value.
        - db: This is the database route you are working with. Its default 
            value is 'data_route' and it can be setted as 'data_backup_route'.

    HOW TO USE:
        - Get a value from the database:
            call read_settings('column_name').
        - Get all the values from the database:
            call read_settings().
        - Get a value from the database backup:
            call read_settings('column_name', 'data_backup_route').
        - Get all the values from the database backup:
            call read_settings(db='data_backup_route').

    RETURNS:
        - If you specify a column name:
            It returns its particular value.
         
        - If you don't specify a column name:
            It returns all the settings values with this format:
                [[column1, column2], (value1, value2)].
    """

    global data_route, data_backup_route

    db_keys = {
            'data_route': data_route,
            'data_backup_route': data_backup_route
            }

    connection = connect(db_keys[db])
    cursor = connection.cursor()
    cursor.execute("SELECT " + column + " FROM settings")

    #Gets a list of all the column names
    column_names = [column_name[0] for column_name in cursor.description]

    #Reads the first row
    values = cursor.fetchone()
    connection.close()

    if column == '*':
        return [column_names, values]
    return values[0]
    

def edit_settings(
        column: str,
        new_value: str
    ):

    """DESCRIPTION:
        - This module allows you to edit an individual value in 
            the settings table.

    PARAMETERS:
        - column: The column that contains the wished editable value.
        - new_value: The new value for the chosen column.

    HOW TO USE:
        - Edit a settings value:
            call edit_settings('column_name', 'new_value').

    RETURNS:
        - Nothing.
        """

    global data_route

    if isfile(data_route):
        connection = connect(data_route)
        cursor = connection.cursor()
        clean_new_value = new_value.replace("'","''")
        cursor.execute("UPDATE settings SET " + column + "='" + str(clean_new_value) + "'")
        connection.commit()
        connection.close() 


def restore_settings():

    """DESCRIPTION:
        - This module restores the database from a backup perviously generated.

    HOW TO USE:
        call restore_settings

    RETURNS:
        - Nothing.
        """

    global data_backup_route

    if isfile(data_backup_route):
        settings = read_settings(db='data_backup_route')

        for x in range(len(settings[0])):
            try:
                edit_settings(settings[0][x], str(settings[1][x]))
            except:
                pass
        edit_settings("active_instance", "0")
        
        #Restore user data
        subtitles = read_scraped_list('subtitles', 'data_backup_route')
        edit_scraped_list('subtitles', 'addition', list_=subtitles)
        
        torrents = read_scraped_list('torrents', 'data_backup_route')
        edit_scraped_list('torrents', 'addition', list_=torrents)
        
        for played_video in read_simple_list("played_videos", "data_backup_route"):
            edit_simple_list("played_videos", played_video, 'add')
        for downloaded_subtitles in read_simple_list("downloaded_subtitles", "data_backup_route"):
            edit_simple_list("downloaded_subtitles", downloaded_subtitles, 'add')
        for torrents_history in read_simple_list("torrents_history", "data_backup_route"):
            edit_simple_list("torrents_history", torrents_history, 'add')
        for newtorrents_history in read_simple_list("newtorrents_history", "data_backup_route"):
            edit_simple_list("newtorrents_history", newtorrents_history, 'add')
        for videos_history in read_simple_list("videos_history", "data_backup_route"):
            edit_simple_list("videos_history", videos_history, 'add')
        for folder_history in read_simple_list("folder_history", "data_backup_route"):
            edit_simple_list("folder_history", folder_history, 'add')
        for words_history in read_simple_list("words_history", "data_backup_route"):
            edit_simple_list("words_history", words_history, 'add')
        for results_history in read_simple_list("results_history", "data_backup_route"):
            edit_simple_list("results_history", results_history, 'add')

    if isfile(data_backup_route):
        system("rm " + data_backup_route)

#######################################################################

def read_scraped_list(
        table: str,
        db:str = 'data_route'
    ):

    """DESCRIPTION:
        - This module reads the scraped list (for torrents or subtitles)
            and its information from the database.

    PARAMETERS:
        - table: This is the table name you're reading. Set it as 'subtitles' or 
            'torrents'.
        - db: This is the database route you are working with. Its default 
            value is 'data_route' and it can be setted as 'data_backup_route'.

    HOW TO USE:
        - Read a list from the database and its information:
            call read_scraped_list(table).
        - Read a list from the database backup and its information:
            call read_scraped_list(table, 'data_backup_route').
        *The table parameter must be replaced by 'subtitles' or 'torrents'.

    RETURNS:
        - It returns a list of tuples containing the registered scraped values
            in the database:
            - For the torrents table:
                [(title_1, seeds_1, leechers_1, platform_1, magnetlink_1, status_1)... (...)].
            - For the subtitles table:
                [(title_1, description_1, url_1, status_1)...(...)]

    """
    global data_route, data_backup_route

    db_keys = {
            'data_route': data_route,
            'data_backup_route': data_backup_route
            }

    connection = connect(db_keys[db])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table)

    #It reads all the values
    values = cursor.fetchall()
    connection.close()

    return values


def edit_scraped_list(
        table: str,
        mode: str = 'current_download', 
        id_: int = None,
        status: int = None,
        list_: list = None
    ):

    """DESCRIPTION:
        - This module edit the scraped list as follows:
            - Edit an element status number.
                - 0: Not downloaded.
                - 1: Downloaded.
                - 2: Last downloaded element (current one).
            - Replace the list.
            - Delete the list.

    PARAMETERS:
        - table: This is the table name you're reading. Set it as 'subtitles' or 
            'torrents'.
        - mode: This paramater specify the action that will be executed by the function.
            - 'edit': Edit an element status (This mode is the default value).
            - 'addition': Add a list of elements to the table..
            - 'clean': Delete all the content of a specified table.
        - id_: ID number of the element you're going to edit its status.
        - status: New status number for the specified element.
        - list_: New list for replacement.

    HOW TO USE:
        - Edit an element status.
            - Mark the current download as a downloaded element (1):
                call edit_scraped_list(table, 'downloaded').
            - Mark an element as the current download (2):
                call edit_scraped_list(table, id_=elemnt_id, status=new_status).
        - Add a list of elements to a table.
            call edit_scraped_list(table, 'addition', list_=elements_list).
                - Subtitles list:
                [[title (str), description (str), url (str), status (int)], ...
                    [...]].
                - Torrents list:
                    [[title (str), seeds (int), leechers (int), platform (str),
                        magnetlink (str), status (int)], ... [...]].
        - Clean a table.
            call edit_scraped_list(table, 'clean').

    RETURNS:
        - Nothing.
"""
    global data_route
    
    if isfile(data_route):
        connection = connect(data_route)
        cursor = connection.cursor()

        #Edit an element status
        if mode == 'current_download':
            cursor.execute("UPDATE " + table + " SET status=2 WHERE rowid=" + \
                    str(id_ + 1))
        elif mode == 'downloaded':
            cursor.execute("UPDATE " + table + " SET status=1 WHERE status=2")

        elif mode == 'clean':
            #Clean the table
            cursor.execute("DELETE FROM " + table)

        #Replace the table
        elif mode == 'addition':

            signs = "?,?,?,?"
            if table == "torrents":
                signs = "?,?,?,?,?,?,?"
            
            cursor.executemany("INSERT INTO " + table + " VALUES (" + signs + ")", list_)

        connection.commit()
        connection.close() 

######################################################################

def read_simple_list(table: str, db:str='data_route'):

    """DESCRIPTION:
        - This module reads a simple list.

    PARAMETERS:
        - table: This is the table name you're reading. Set it as 'downloaded_subtitles' or
            'played_videos'.

    HOW TO USE:
        - Read a list from the database and its information:
            call read_simple_list(table).
            *The table parameter must be replaced by 'subtitles' or 'torrents'.

    RETURNS:
        - It returns a list of tuples containing the registered scraped values
    global data_route

"""
    global data_route, data_backup_route

    db_keys = {
            'data_route': data_route,
            'data_backup_route': data_backup_route
            }

    connection = connect(db_keys[db])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table)

    values = cursor.fetchall()
    connection.close()

    ##################################################
    if table == 'played_videos':
        # Delete URIs that point to deleted videos
        played_list = []
        for value in values:
            if isfile(value[0]):
                played_list.append(value[0])
            else:
                edit_simple_list(table, value[0])
        return played_list
    ##################################################

    return [value[0] for value in values]

def edit_simple_list(table: str, value: str=None, mode: str='delete'):

    """DESCRIPTION:
        - This module edit a simple list, you can:
            - Delete a table.
            - Delete an element of a table.
            - Add an element to a table.

    PARAMETERS:
        - table: This is the table name you're reading. Set it as 'downloaded_subtitles' or
            'played_videos'.
        - value: The value you want to delete. If you don't specify it, the module will clear
            the table.
        - mode: This paramater specify the action that will be executed by the function.
            - 'delete': Its the default mode and you can detele a table or a row with it.
            - 'add': You can add an element to a table with it.

    HOW TO USE:
        - Delete an element:
            call edit_simple_list(table, value_to_delete).
        - Clear a table:
            call edit_simple_list(table).
        - Add an element:
            call edit_simple_list(table,value,'add').
    """
    
    if isfile(data_route):
        connection = connect(data_route)
        cursor = connection.cursor()

        column_name = table[table.index("_")+1:]

        # Delete an element or clear a table
        if mode == 'delete':
            # The command_complement determines the deletion:
            # one row or the complete table
            command_complement = ''
            if value != None:
                command_complement = ' WHERE ' + column_name + "='" + value + "'"

            sentence = "DELETE FROM " + table + command_complement

        # Add an element
        elif mode == 'add':
            clean_value = value.replace("'","''")
            sentence = "INSERT INTO " + table + " (" + column_name + ") VALUES ('" + clean_value + "')"

        cursor.execute(sentence)

        connection.commit()
        connection.close() 

######################################################################
