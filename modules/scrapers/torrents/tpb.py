#!/bin/env python

from tpblite import TPB, ORDERS, CATEGORIES

def tpb(search):

    # TPB object with the default domain
    t = TPB('https://tpb.party')

    # Getting the data
    torrents = t.search(search, order=ORDERS.SEEDERS.DES, \
            category=CATEGORIES.VIDEO.MOVIES)

    torrent_list = [[torrent.title, torrent.filesize, torrent.seeds, \
            torrent.leeches, "TPB", torrent.magnetlink] \
            for torrent in torrents]

    return torrent_list
