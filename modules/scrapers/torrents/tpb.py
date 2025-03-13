#!/bin/env python


from requests import Session
from urllib.parse import quote

from modules.rows_from_text_file import rows_from_text_file
from modules.admin_db import edit_scraped_list, read_settings, edit_settings


"""
It gets a string search, for example: the happy dog
It returns a torrents list with the following format:
[[str_title_1, str_filesize_1, int_seeds_1, str_leechers_1, \
        "TPB", str_magnetlink_1, 0], [str_title_2, ...]...]
"""


def tpb(search_words):

    url = f"https://apibay.org/q.php?q={quote(search_words.strip())}&cat=200"
    session = Session()
    request = session.get(url)
    trackers = rows_from_text_file('trackers.txt')

    if request.status_code != 200:
        finished = read_settings("run_animation") + 1
        edit_settings("run_animation", str(finished))
        return

    torrents = [[
        torrent['name'],
        bytes_to_legible(torrent['size']),  # String
        int(torrent['seeders']),
        int(torrent['leechers']),
        "TPB",
        (
            f"magnet:?xt=urn:btih:{(torrent['info_hash'])}&"
            f"dn={quote(torrent['name'])}&tr={quote('&tr='.join(trackers))}"
        ),
        0
    ] for torrent in request.json()]

    edit_scraped_list('torrents', 'addition', list_=torrents)
    finished = read_settings("run_animation") + 1
    edit_settings("run_animation", str(finished))


def bytes_to_legible(size):

    size = int(size)
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    index = 0

    while size >= 1024 and index < len(units) - 1:
        size /= 1024.0
        index += 1

    return f"{size:.2f} {units[index]}"
