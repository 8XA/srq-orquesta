#!/bin/env python

from threading import Thread
from modules.scrapers.torrents.nyaa import nyaa
from modules.scrapers.torrents.tpb import tpb
from modules.admin_db import edit_scraped_list, read_scraped_list, edit_settings, read_settings
from modules.suggested_search import suggested_search
from ascii_animations.cinema.ascii import ascii_animation
from os import system
from time import sleep
from scrapimdb import ImdbSpider

def torrent_master(raw_search:str):
    """
    It gets a search sentence, and it updates the database with the torrents founded.
    """

    #It cleans the database
    edit_scraped_list('torrents', 'clean')

    #ASCII animation
    ascii_thread = Thread(
            target=ascii_animation,
            args=("Buscando torrents...", 2),
        )
    ascii_thread.start()

    #Words for scraping
    if read_settings('torrent_words_mode') == 'original':
        suggested = suggested_search(raw_search)
        try:
            imdb_info = ImdbSpider(suggested)
            original_search = imdb_info.get_original_title()
            if ':' in original_search:
                original_search = original_search[:original_search.index(':')]
        except Exception as e:
            original_search = suggested
        edit_settings('torrent_words', original_search)
    elif read_settings('torrent_words_mode') == 'suggested':
        edit_settings('torrent_words', suggested_search(raw_search))
    else:
        edit_settings('torrent_words', raw_search)
    search = read_settings('torrent_words')

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
    ascii_thread.join()
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
    
    else:
        system("clear")
        print("Ningún torrent hallado...")
        sleep(2)

