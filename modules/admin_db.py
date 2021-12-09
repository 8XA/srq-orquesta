#!/bin/env python

#This module has the functions to read and edit the database and its backup

from sqlite3 import connect
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
            call settings_read('column_name').
        - Get all the values from the database:
            call settings_read().
        - Get a value from the database backup:
            call settings_read('column_name', 'data_backup_route').
        - Get all the values from the database backup:
            call settings_read(db='data_backup_route').

    RETURNS:
        - If you specify a column name:
            It returns its particular value.
         
        - If you don't specify a column name:
            It return all the settings values with this format:
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
        cursor.execute("UPDATE settings SET " + column + "='" + str(new_value) + "'")
        connection.commit()
        connection.close() 

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
        - It returns the scraped list:
            For the torrents table:
                [(title_1, seeds_1, leechers_1, platform_1, magnetlink_1, status_1)... (...)].
            For the subtitles table:
                [(title_1, description_1, url_1, status_1)...(...)]
                *This is a list of tuples containing the values.

    """
    global data_route, data_backup_route

    db_keys = {
            'data_route': data_route,
            'data_backup_route': data_backup_route
            }

    connection = connect(db_keys[db])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table)

    #Reads the first row
    values = cursor.fetchall()
    connection.close()

    return values


def edit_scraped_list(
        table: str,
        mode: str = 'edit', 
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
            - 'replace': Replace all the content of a specified table by another list.
            - 'clean': Delete all the content of a specified table.
        - id_: ID number of the element you're going to edit its status.
        - status: New status number for the specified element.
        - list_: New list for replacement.

    HOW TO USE:
        - Edit an element status.
            call edit_scraped_list(table, id_=elemnt_id, status=new_status).
        - Replace a table content.
            call edit_scraped_list(table, 'replace', list_=new_list).
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
        if mode == 'edit':
            cursor.execute("UPDATE " + table + " SET status=" + str(status) + \
                    " WHERE rowid=" + str(id_ + 1))

        elif mode in ['replace', 'clean']:
            #Clean the table
            cursor.execute("DELETE FROM " + table)

            #Replace the table
            if mode == 'replace':

                signs = "?,?,?,?"
                if table == "torrents":
                    signs = "?,?,?,?,?,?"
                
                cursor.executemany("INSERT INTO " + table + " VALUES (" + signs + ")", list_)

        connection.commit()
        connection.close() 

######################################################################
#
##leer_lista_simple
##editar_lista_simple
##  -- Agregar elemento a la lista
##  -- Eliminar elemento de la lista
##  -- Limpiar tabla
##
##RESTAURAR
##
