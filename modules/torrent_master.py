#!/bin/env python

from threading import Thread
from modules.scrapers.torrents.nyaa import nyaa
from modules.scrapers.torrents.tpb import tpb
from modules.admin_db import edit_scraped_list, read_scraped_list

def torrent_master(search:str):
    """
    It gets a search sentence, and it updates the database with the torrents founded.
    """
    #It cleans the database
    edit_scraped_list('torrents', 'clean')
    
    #It gets torrents from all scrapers
    nyaa_thread = Thread(
            target=nyaa,
            args=(search,),
            daemon=True
        )
    
    tpb_thread = Thread(
            target=tpb,
            args=(search,),
            daemon=True
        )

    nyaa_thread.start()
    tpb_thread.start()
    nyaa_thread.join()
    tpb_thread.join()

    #Disordered torrents
    torrent_results = read_scraped_list('torrents')

    if len(torrent_results) > 0:
        #The clean list without torrents without seeds
        torrent_results = [torrent for torrent in torrent_results if torrent[2] > 0]

        #Sort torrents
        iterate = True
        while iterate:
            iterate = False
            for index in range(len(torrent_results)):
                if index > 0:
                    if torrent_results[index][2] >= torrent_results[index-1][2]:
                        if torrent_results[index][2] > torrent_results[index-1][2] or \
                                torrent_results[index][3] > torrent_results[index-1][3]:
                            torrent_results[index-1:index+1] = reversed(torrent_results[index-1:index+1])
                            iterate = True

        #Update database
        edit_scraped_list('torrents', 'clean')
        edit_scraped_list('torrents','addition', list_=torrent_results)

