#!/bin/env python 

from os import system
from termcolor import colored
from modules.menu import menu
from modules.torrent_master import torrent_master
from modules.refresh_history import refresh_history
from modules.admin_db import read_settings, edit_settings, edit_simple_list, read_simple_list
from modules.columns_number import columns_number_func
from modules.strings_fitting import phrase_fitting, \
        centered_phrase_fitting, colored_centered_filter 
from modules.admin_db import read_scraped_list, edit_scraped_list

def torrents():
    edit_settings("previous_menu", str(read_settings("menu")))
    edit_settings("menu","torrents")

    title = "TORRENTS"
    rpp = read_settings("results_per_page")
    page = 1

    while True:
        torrent_results = read_scraped_list('torrents')
        
        table = 'torrents_history' 
        if len(torrent_results) == 0:
            table = 'new' + table
        refresh_history(table)

        columns_number = columns_number_func()
        filters = " ".join(read_settings('torrents_filter').split(','))
        filters = filters.split(" ")
        while '' in filters:
            filters.remove('')

        # Download ID assigned
        torrent_results_ids = [[id_] + list(torrent_results[id_]) for id_ in \
                range(len(torrent_results))]

        filtered_torrents = [torrent for torrent in torrent_results_ids if \
                len([word for word in filters if word.lower() in \
                (torrent[1] + " " + torrent[5]).lower()]) == len(filters)]

        red_line_ = colored(columns_number*"-", 'red', attrs=['bold', 'dark'])
        red_line = colored(columns_number*"=", 'red', attrs=['bold', 'dark'])
        yellow_line = colored(columns_number*"=", 'yellow', attrs=['bold', 'dark'])
        blue_line = colored(columns_number*"=", 'blue', attrs=['bold', 'dark'])

        print(blue_line)
        print(((columns_number-len(title))//2)*" " + title)
        print(blue_line)
        print(yellow_line)
        if len(torrent_results) == 0:
            print()
            print(phrase_fitting(columns_number, "Realiza una búsqueda..."))
            print()
            print(yellow_line)
        elif len(filtered_torrents) == 0:
            print()
            print(phrase_fitting(columns_number, "Ningún torrent coincide. Prueba con otro filtro..."))
            print()
            print(yellow_line)

        # Torrents numbered for print them in pages
        numbered_filtered_torrents = [filtered_torrents[id_] + [id_]  for \
                id_ in range(len(filtered_torrents))]

        # Total number of pages
        total_pages = len(numbered_filtered_torrents)//rpp
        if total_pages*rpp < len(numbered_filtered_torrents):
            total_pages += 1
        if total_pages == 0:
            total_pages = 1

        # Torrents of the current page
        page_torrents = numbered_filtered_torrents[(page-1)*rpp:page*rpp]

        #Print the torrents of the current page
        for iterator in range(len(page_torrents)-1,-1,-1):
            # Background for downloaded torrents
            background = 'on_red'
            if page_torrents[iterator][7] == 2:
                background = 'on_white'
            if page_torrents[iterator][7] != 0:
                ID = colored("ID ", 'cyan', background, attrs=['bold', 'dark']) + \
                        colored(page_torrents[iterator][0], 'green', background, \
                        attrs=['bold', 'dark'])
            else:
                ID = colored("ID ", 'cyan', attrs=['bold', 'dark']) + \
                        colored(page_torrents[iterator][0], 'green', \
                        attrs=['bold', 'dark'])


            print(str(page_torrents[iterator][8]) + ": " + ID + " -> " + page_torrents[iterator][1])
            print(columns_number * "-")
            print("size: " + str(page_torrents[iterator][2]))
            print("seeds: " + str(page_torrents[iterator][3]))
            print("leechers: " + str(page_torrents[iterator][4]))
            platform = page_torrents[iterator][5]
            colored_platform = colored(platform, 'cyan', attrs=['bold'])
            print((columns_number - len(platform)) * " " + colored_platform)
            print(yellow_line)


        #Print the words used for searching
        print(red_line)
        if read_settings('new_torrent_search') == 0:

            search_words = "Palabras de búsqueda:"
            printable_row_search = colored(centered_phrase_fitting(columns_number, search_words), 'white', attrs=['bold'])
            spaces_number = columns_number - 6 - (((columns_number - len(search_words))//2) + len(search_words))
            
            #Exact search
            ex = colored("ex", 'green', attrs=['dark','bold'])
            #Suggested search
            su = colored("su", 'green', attrs=['dark','bold'])
            
            search_to_color ={
                    'exact': ex,
                    'suggested': su
                }

            mode = read_settings('torrent_words_mode')
            search_to_color[mode] = colored(search_to_color[mode], on_color='on_white')
            
            printable_row_search += spaces_number * " " + search_to_color['exact'] + " " + search_to_color['suggested']
            print(printable_row_search)

            for row in phrase_fitting(columns_number, read_settings('torrent_words')).split("\n"):
                printable_row = row + (columns_number - len(row)) * " "
                printable_row = colored(printable_row, 'grey', 'on_white', attrs=['bold','dark'])
                print(printable_row)
            print(red_line_)

        #Print filters
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

        #Downloadable torrents
        downloadables_dict = {
            "page": page_torrents,
            "avaliables": torrent_results_ids,
            "filtered": filtered_torrents
            }

        downloadable_ids = [torrent[0] for torrent in \
                downloadables_dict[read_settings('downloadable_ids')]]

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
        elif i[1].upper() in ["EX","SU"]:
            mode_dict = {
                    "EX": "exact",
                    "SU": "suggested"
                }
            edit_settings('torrent_words_mode', mode_dict[i[1].upper()])
        elif len(torrent_results) == 0:
            #history
            edit_settings('new_torrent_search', '0')
            edit_simple_list(table, i[1],'add')
            try:
                #Search torrents and save it in database
                torrent_master(i[1])
                system("clear")

            except:
                pass
        elif i[1].isdigit() and int(i[1]) in downloadable_ids:
            edit_scraped_list('torrents', 'downloaded')
            edit_scraped_list('torrents', id_=int(i[1]), status=2)
            system("xdg-open '" + torrent_results_ids[int(i[1])][6] + "'")
            return 'videos'
        else:
            edit_simple_list('torrents_history', i[1],'add')
            edit_settings("torrents_filter", i[1])
