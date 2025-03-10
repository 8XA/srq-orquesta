#!/bin/env python

from requests import get
from urllib.parse import quote
from modules.rows_from_text_file import rows_from_text_file
from modules.admin_db import edit_scraped_list, edit_settings, read_settings


def yts(search:str):
    url = f"https://yts.mx/api/v2/list_movies.json?query_term={ quote(search) }&limit=50"
    yts_response = get(url)
    if yts_response.status_code == 200:

        #Trackers
        trackers = rows_from_text_file('trackers.txt')

        torrent_list = list()
        if 'movies' in yts_response.json()['data'].keys():
            for movie in yts_response.json()['data']['movies']:
                for torrent in movie['torrents']:
                    torrent_base = ['', '', 0, 0, 'YTS', '', 0]
                    
                    dot = str()
                    year = str()
                    if str(movie['year']) not in movie['title_long']:
                        dot = '.'
                        year = movie['year']

                    torrent_base[0] = f"{ movie['title_long'] }{ dot }{ year }.{ torrent['quality'] }"
                    torrent_base[1] = torrent['size']
                    torrent_base[2] = torrent['seeds']
                    torrent_base[3] = torrent['peers']
                    torrent_base[5] = f"magnet:?xt=urn:btih:{ torrent['hash'] }&dn={ quote(torrent_base[0]) }&tr={ '&tr='.join(trackers) }"

                    torrent_list.append(torrent_base)

        if len(torrent_list) > 0:
            edit_scraped_list('torrents','addition', list_=torrent_list)

    finished = read_settings("run_animation") + 1
    edit_settings("run_animation", str(finished))

