#!/bin/env python

from os import popen
from threading import Thread

def nyaa(search:str):
    """
    It gets a string search, for example: the happy dog
    It returns a founded torrents list with the format as follows:
    [[str_title_1, str_filesize_1, int_seeds_1, str_leechers_1, \
            "NYAA", str_magnetlink_1], [str_title_2, ...]...]
    """

    torrent_dict = {}

    first_search = nyaa_onepage(search, 1, True)
    numb_of_pages = first_search[1]
    torrent_list = first_search[0]

    current_page = 1
    threads_dict = {}
    while current_page < numb_of_pages:

        current_page += 1

        torrent_list += nyaa_onepage(search, current_page)

#        threads_dict[current_page] = Thread(
#                target=nyaa_onepage,
#                args=(search, current_page)
#            )
#        
#        threads_dict[current_page].start()
#        threads_dict[current_page].join()
#    
#    keys = [key for key in torrent_dict]
#    keys.sort()
#
#    torrent_list = []
#    for key in keys:
#        torrent_list += torrent_dict[key]
    return torrent_list


def nyaa_onepage(
        search:str,
        page_number:int,
        read_pages_number:bool=False
    ):

    words_sum = "+".join(search.split(" "))
    words_sum = words_sum.replace("'","%27")

    search_url = "https://nyaa.si/?f=0&c=0_0&q=" + words_sum + "&s=seeders&o=desc&p=" + str(page_number)
    raw_result = popen("curl -L '" + search_url + "' | iconv -f iso-8859-1 -t utf-8").read()

    torrent_list = []
    while "magnet:?xt=" in raw_result:
        torrent = ['', '', 0, 0, 'NYAA', '']

        magnet_index_0 = raw_result.index("magnet:?xt=")
        magnet_index_1 = raw_result[magnet_index_0:].index('">') + magnet_index_0
        torrent[5] = raw_result[magnet_index_0: magnet_index_1]

        title_index_0 = raw_result.rindex('title="', 0, magnet_index_0)
        title_index_1 = raw_result[title_index_0:].index('">') + title_index_0
        torrent[0] = raw_result[title_index_0 + 7: title_index_1]

        size_index_0 = raw_result[magnet_index_1:].index('class="text-center">') + magnet_index_1
        size_index_1 = raw_result[size_index_0 + 20:].index("</t") + size_index_0
        torrent[1] = raw_result[size_index_0 + 20: size_index_1 + 20]

        seeders_index_0 = raw_result[size_index_1:].index('class="text-center">') + size_index_1
        seeders_index_1 = raw_result[seeders_index_0 + 20:].index("</t") + seeders_index_0
        torrent[2] = raw_result[seeders_index_0 + 20: seeders_index_1 + 20]

        leechers_index_0 = raw_result[seeders_index_1:].index('class="text-center">') + seeders_index_1
        leechers_index_1 = raw_result[leechers_index_0 + 20:].index("</t") + leechers_index_0
        torrent[3] = raw_result[leechers_index_0 + 20: leechers_index_1 + 20]

        torrent_list.append(torrent)
        raw_result = raw_result[leechers_index_1:]

    numb_of_torrents = 0
    if read_pages_number == True:
        numb_of_torrents_0 = raw_result.index('">Displaying results')
        numb_of_torrents_1 = raw_result[numb_of_torrents_0 + 20:].index('results') + numb_of_torrents_0
        numb_of_torrents = raw_result[numb_of_torrents_0 + 20: numb_of_torrents_1 + 20]
        numb_of_torrents = numb_of_torrents.split(" ")
        numb_of_torrents = int(numb_of_torrents[4])
    numb_of_pages = numb_of_torrents/75

    if read_pages_number == True:
        return torrent_list, numb_of_pages
    return torrent_list
