#!/bin/env python

from tpblite import TPB, ORDERS, CATEGORIES
from threading import Thread

def tpb(search):
    """
    It gets a string search, for example: the happy dog
    It returns a founded torrents list with the format as follows:
    [[str_title_1, str_filesize_1, int_seeds_1, str_leechers_1, \
            "TPB", str_magnetlink_1], [str_title_2, ...]...]
    """
    global global_torrent_list, flag
    
    global_torrent_list = []
    thread_dict = {}
    flag = True

    counter = 0
    while flag:
        for x in range(10):
            counter += 1

            thread_dict[counter] = Thread(
                    target=tpb_onepage,
                    args=(search, counter),
                    daemon=True
                )
            thread_dict[counter].start()
        
        for key in thread_dict:
            thread_dict[key].join()

    return global_torrent_list


def tpb_onepage(search, page):
    global global_torrent_list, flag

    # TPB object with the default domain
    t = TPB()

    # Getting the data
    torrents = t.search(search, order=ORDERS.SEEDERS.DES, category=CATEGORIES.VIDEO.ALL, page=page)

    torrent_list = [[torrent.title, torrent.filesize, torrent.seeds, \
            torrent.leeches, "TPB", torrent.magnetlink] \
            for torrent in torrents]
    global_torrent_list += torrent_list
    
    if 0 in [torrent.seeds for torrent in torrents]:
        flag = False

