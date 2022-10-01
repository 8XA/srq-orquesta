#!/bin/env python

from modules.admin_db import edit_scraped_list, read_settings, edit_settings
from modules.rows_from_text_file import rows_from_text_file
from tpblite import TPB, ORDERS, CATEGORIES
from threading import Thread

def tpb(search):
    """
    It gets a string search, for example: the happy dog
    It returns a founded torrents list with the format as follows:
    [[str_title_1, str_filesize_1, int_seeds_1, str_leechers_1, \
            "TPB", str_magnetlink_1], [str_title_2, ...]...]
    """
    global global_torrent_list_tpb, flag
    
    try:
        global_torrent_list_tpb = []
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

        torrent_list = [torrent for torrent in global_torrent_list_tpb if torrent[2] > 0]

        #To the database
        edit_scraped_list('torrents','addition', list_=torrent_list)

    except Exception as e:
        pass

    finished = read_settings("run_animation") + 1
    edit_settings("run_animation", str(finished))


def tpb_onepage(search, page):
    global global_torrent_list_tpb, flag

    try:
        # TPB object with the default domain
        t = TPB()
        trackers = rows_from_text_file('trackers.txt')

        # Getting the data
        torrents = t.search(search, order=ORDERS.SEEDERS.DES, category=CATEGORIES.VIDEO.ALL, page=page)

        torrent_list = [[torrent.title, torrent.filesize, torrent.seeds, \
                torrent.leeches, "TPB", f"{ torrent.magnetlink }&tr={ '&tr='.join(trackers) }", 0] \
                for torrent in torrents]
        global_torrent_list_tpb += torrent_list
        
        if 0 in [torrent.seeds for torrent in torrents]:
            flag = False
    except:
        flag = False

