#!/bin/env python 

from os import system
from termcolor import colored
from modules.menu import menu
from modules.scrapers.torrents.tpb import tpb
from modules.admin_db import read_settings, edit_settings
from modules.columns_number import columns_number_func
from modules.strings_fitting import centered_phrase_fitting
from modules.admin_db import read_scraped_list, edit_scraped_list

def torrents():
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","torrents")

    columns_number = columns_number_func()
    rpp = read_settings("results_per_page")
    torrent_results = read_scraped_list('torrents')
    filters = read_settings('torrents_filter').split(',')
    system("clear")

    red_line = colored(columns_number*"=", 'red', attrs=['bold', 'dark'])
    yellow_line = colored(columns_number*"=", 'yellow', attrs=['bold', 'dark'])
    blue_line = colored(columns_number*"=", 'blue', attrs=['bold', 'dark'])

    title = "TORRENTS"
    print(blue_line)
    print(((columns_number-len(title))//2)*" " + title)
    print(blue_line)
    print(yellow_line)

    torrent_results_ids = [[id_] + list(torrent_results[id_]) for id_ in \
            range(len(torrent_results))]

    filtered_torrents = [torrent for torrent in torrent_results_ids if \
            len([word for word in filters if word.lower() in \
            (torrent[1] + " " + torrent[5]).lower()]) == len(filters)]

    for iterator in range(len(filtered_torrents)-1,-1,-1):
        # Background for downloaded torrents
        background = 'on_red'
        if filtered_torrents[iterator][7] == 2:
            background = 'on_white'
        if filtered_torrents[iterator][7] != 0:
            ID = colored("ID ", 'cyan', background, attrs=['bold', 'dark']) + \
                    colored(filtered_torrents[iterator][0], 'green', background, \
                    attrs=['bold', 'dark'])
        else:
            ID = colored("ID ", 'cyan', attrs=['bold', 'dark']) + \
                    colored(filtered_torrents[iterator][0], 'green', \
                    attrs=['bold', 'dark'])


        print(str(iterator) + ": " + ID + " -> " + filtered_torrents[iterator][1])
        print(columns_number * "-")
        print("size: " + str(filtered_torrents[iterator][2]))
        print("seeds: " + str(filtered_torrents[iterator][3]))
        print("leechers: " + str(filtered_torrents[iterator][4]))
        platform = filtered_torrents[iterator][5]
        colored_platform = colored(platform, 'cyan', attrs=['bold'])
        print((columns_number - len(platform)) * " " + colored_platform)
        print(yellow_line)


    #Imprime filtros
    print(red_line)
    print(colored(centered_phrase_fitting(columns_number, "Filtros:"), 'white', attrs=['bold']))
    print(red_line)

    i = menu(columns_number, "Busca, filtra o elige un torrent")

    if i[0] == "menu":
        return i[1]
    else:
        crudo = [torrent + [0] for torrent in tpb(i[1])]
        edit_scraped_list('torrents','replace', list_=crudo)
        input("...")

        return 'torrents'


#enter avanza pagina
#.. retocede pagina
#ns = nueva busqueda
#
#numero dentro de (disponibles, descargables, etc.):
#    ejecuta torrent
#    marca los subs descargados anteriores en uno
#    marca sub como descargado
#
#cualquier otra cosa hace las veces de filtro
