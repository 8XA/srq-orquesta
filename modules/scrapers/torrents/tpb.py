#!/bin/env python

from tpblite import TPB, ORDERS, CATEGORIES

def tpb(search):

    # TPB object with the default domain
    t = TPB()

    # Getting the data
    torrents = t.search(search, order=ORDERS.SEEDERS.DES, category=CATEGORIES.VIDEO.ALL)

    torrent_list = [[torrent.title, torrent.filesize, torrent.seeds, \
            torrent.leeches, "TPB", torrent.magnetlink] \
            for torrent in torrents]

    return torrent_list
