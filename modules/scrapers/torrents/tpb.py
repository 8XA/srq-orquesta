#!/bin/env python

from tpblite import TPB, ORDERS, CATEGORIES

def tpb(busqueda):

    #Objeto TPB con dominio por defecto
    t = TPB()

    #Recopilación de datos
    torrents = t.search(busqueda, order=ORDERS.SEEDERS.DES, category=CATEGORIES.VIDEO.MOVIES)

    lista = [[torrent.title, torrent.filesize, torrent.seeds, \
            torrent.leeches, "TPB", torrent.magnetlink] \
            for torrent in torrents]

    return lista
