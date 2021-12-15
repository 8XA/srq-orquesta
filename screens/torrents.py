#!/bin/env python 

from os import system
from termcolor import colored
from modules.menu import menu
from modules.scrapers.torrents.tpb import tpb
from modules.admin_db import read_settings, edit_settings
from modules.columns_number import columns_number_func
from modules.strings_fitting import centered_phrase_fitting, colored_centered_filter
from modules.admin_db import read_scraped_list, edit_scraped_list

def torrents():
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","torrents")

    title = "TORRENTS"
    rpp = read_settings("results_per_page")
    page = 1

    while True:
        columns_number = columns_number_func()
        torrent_results = read_scraped_list('torrents')
        filters = " ".join(read_settings('torrents_filter').split(','))
        filters = filters.split(" ")
        while '' in filters:
            filters.remove('')
        
        red_line = colored(columns_number*"=", 'red', attrs=['bold', 'dark'])
        yellow_line = colored(columns_number*"=", 'yellow', attrs=['bold', 'dark'])
        blue_line = colored(columns_number*"=", 'blue', attrs=['bold', 'dark'])

        print(blue_line)
        print(((columns_number-len(title))//2)*" " + title)
        print(blue_line)
        print(yellow_line)

        # Download ID assigned
        torrent_results_ids = [[id_] + list(torrent_results[id_]) for id_ in \
                range(len(torrent_results))]

        filtered_torrents = [torrent for torrent in torrent_results_ids if \
                len([word for word in filters if word.lower() in \
                (torrent[1] + " " + torrent[5]).lower()]) == len(filters)]

        # Torrents numbered for print them in pages
        numbered_filtered_torrents = [[id_] + filtered_torrents[id_] for \
                id_ in range(len(filtered_torrents))]

        # Total number of pages
        total_pages = len(numbered_filtered_torrents)//rpp
        if total_pages*rpp < len(numbered_filtered_torrents):
            total_pages += 1

        # Torrents of the current page
        page_torrents = numbered_filtered_torrents[(page-1)*rpp:page*rpp]

        #Print the torrents of the current page
        for iterator in range(len(page_torrents)-1,-1,-1):
            # Background for downloaded torrents
            background = 'on_red'
            if page_torrents[iterator][8] == 2:
                background = 'on_white'
            if page_torrents[iterator][8] != 0:
                ID = colored("ID ", 'cyan', background, attrs=['bold', 'dark']) + \
                        colored(page_torrents[iterator][1], 'green', background, \
                        attrs=['bold', 'dark'])
            else:
                ID = colored("ID ", 'cyan', attrs=['bold', 'dark']) + \
                        colored(page_torrents[iterator][1], 'green', \
                        attrs=['bold', 'dark'])


            print(str(page_torrents[iterator][0]) + ": " + ID + " -> " + page_torrents[iterator][2])
            print(columns_number * "-")
            print("size: " + str(page_torrents[iterator][3]))
            print("seeds: " + str(page_torrents[iterator][4]))
            print("leechers: " + str(page_torrents[iterator][5]))
            platform = page_torrents[iterator][6]
            colored_platform = colored(platform, 'cyan', attrs=['bold'])
            print((columns_number - len(platform)) * " " + colored_platform)
            print(yellow_line)


        #Print filters
        print(red_line)
        
        print(colored(centered_phrase_fitting(columns_number, \
                "Filtros:"), 'white', attrs=['bold']))

        colored_filters = colored_centered_filter(columns_number, \
                "  ".join(filters))
        
        if len(filters) > 0:
            print(colored_filters)
        print(red_line)

        i = menu(columns_number, "Página " + str(page) + \
                " de "+ str(total_pages) + " - " + \
                str(len(filtered_torrents)) + " torrents")

        if i[0] == "menu":
            return i[1]
        elif i[1] == '':
            page += 1
            if page > total_pages:
                page = 1
        elif i[1] == '..':
            page -= 1
            if page < 1:
                page = total_pages
        else:
            edit_settings("torrents_filter", i[1])

#            crudo = [torrent + [0] for torrent in tpb(i[1])]
#            edit_scraped_list('torrents','replace', list_=crudo)



#ns = nueva busqueda
#
#numero dentro de (disponibles, descargables, etc.):
#    ejecuta torrent
#    marca los subs descargados anteriores en uno
#    marca sub como descargado
