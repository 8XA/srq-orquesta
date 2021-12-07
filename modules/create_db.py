#!/bin/env python

from sqlite3 import connect
from os.path import isfile

def create_db():
    """
    This module creates the database if this doesn't exist.
    *The function doesn't take any parameter.

    Boolean values in the database:
    -----
    0: False
    1: True
    -----
    """
    route = "/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/data.db"

    if isfile(route):
        return "Exist"
    else:
        connection = connect(route)
        cursor = connection.cursor()

#        #TABLES
#        ##################################################
#        
#        #Tabla torrents hallados y sus características
#        cursor.execute("CREATE TABLE torrents (" \
#                #Nombre del torrent
#                "titulo TEXT, " \
#                #Número de sembradores del torrent
#                "seeds INTEGER, " \
#                #Número de sanguijuelas
#                "leechers INTEGER, " \
#                #Plataforma de donde se obtuvo el torrent
#                "procedencia TEXT, " \
#                #Enlace magnético
#                "magnetlink TEXT, " \
#                #Estado:
#                    #0: No descargado
#                    #1: Descargado
#                    #2: Último descargado (actual)
#                "status INTEGER " \
#                ")")
#
#        ##################################################
#
#        #Lista de subtítulos hallados y sus características
#        cursor.execute("CREATE TABLE subtitulos (" \
#                #Nombre del subtítulo
#                "titulo TEXT, " \
#                #Descripción del subtítulo
#                "descripcion TEXT, " \
#                #URL del subtítulo
#                "url TEXT, " \
#                #Estado:
#                    #0: No descargado
#                    #1: Descargado
#                    #2: Último descargado (actual)
#                "status INTEGER " \
#                ")")
#
#        ##################################################

        #Settings table
        cursor.execute("CREATE TABLE settings (" \
                #SETTINGS
                #Automatic update when the software starts
                "auto_update INTEGER, " \
                #Automatic start when you run Termux
                "auto_start INTEGER, " \
                #The scrapers you'll use for subs
                "sub_getters TEXT, " \
                #The scrapers you'll use for torrents
                "torrent_getters TEXT, " \
                #Recode subs to UTF-8
                "recode INTEGER, " \
                #One row per list element on the screens
                "one_line INTEGER, " \
                #Admited video extensions on the 'Videos' screen
                "extensions TEXT, "  \
                #Downloadable IDs for torrents and subs
                "downloadable_ids TEXT, "  \
                #Results per page for torrents and subs
                "results_per_page INTEGER, " \

                #TEMPORARY SETTINGS
                #True if there is a SRQ ORQUESTA instance running
                "active_instance INTEGER, " \
                #Subtitle download URL
                "sub_download_url TEXT, " \
                #Folder route
                "folder_route TEXT, " \
                #Selected video name
                "selected_video TEXT, " \
                #Current menu name
                "menu TEXT, " \
                #Previous menu name
                "previous_menu TEXT, " \
                #True if the subtitle search has changed
                "sub_search_changed INTEGER, " \
                #True if the torrent search has changed
                "torrent_search_changed INTEGER, " \
                #The words that will be used for the subs search
                "sub_words TEXT, " \
                #The words that will be used for the torrents search
                "torrent_words TEXT, " \
                #Filter for the torrent results
                "torrents_filter TEXT, " \
                #Filter for the video list
                "videos_filter TEXT, " \
                #Filter for the sub results
                "subs_filter TEXT " \
                ")")

        #Default values for settings
        cursor.execute("INSERT INTO settings (auto_update) VALUES (1)")
        cursor.execute("UPDATE settings SET auto_start = 1")
        cursor.execute("UPDATE settings SET sub_getters = 'subdivx'")
        cursor.execute("UPDATE settings SET torrent_getters = 'tpb,yts,rarbg'")
        cursor.execute("UPDATE settings SET recode = 0")
        cursor.execute("UPDATE settings SET one_line = 1")
        cursor.execute("UPDATE settings SET extensions = 'avi,mp4,mkv'")
        cursor.execute("UPDATE settings SET downloadable_ids = 'disponibles'")
        cursor.execute("UPDATE settings SET results_per_page = 50")

        #Default values for temporary settings
        cursor.execute("UPDATE settings SET active_instance = 0")
        cursor.execute("UPDATE settings SET sub_download_url = ''")
        cursor.execute("UPDATE settings SET folder_route = '/sdcard/'")
        cursor.execute("UPDATE settings SET selected_video = ''")
        cursor.execute("UPDATE settings SET menu = 'videos'")
        cursor.execute("UPDATE settings SET previous_menu = ''")
        cursor.execute("UPDATE settings SET sub_search_changed = 0")
        cursor.execute("UPDATE settings SET torrent_search_changed = 0")
        cursor.execute("UPDATE settings SET sub_words = ''")
        cursor.execute("UPDATE settings SET torrent_words = ''")
        cursor.execute("UPDATE settings SET torrents_filter = ''")
        cursor.execute("UPDATE settings SET videos_filter = ''")
        cursor.execute("UPDATE settings SET subs_filter = ''")

        ##################################################

#        #Lista de videos reproducidos
#        #Marca el contenido de esta lista en la sección 'Videos'
#        cursor.execute("CREATE TABLE videos_reproducidos (" \
#                #Video reproducido con ruta
#                "video TEXT " \
#                ")")
#
#        ##################################################
#
#        #Lista subtítulos descargados
#        #Auxiliar al eliminar carpetas de torrent vacías
#        cursor.execute("CREATE TABLE subtitulos_descargados (" \
#                #Subtítulo descargado con ruta
#                "sub TEXT " \
#                ")")
#
#        ##################################################

        connection.commit()
        connection.close()

        return "Created"

