#!/bin/env python


from requests import Session
from random import sample

from modules.rows_from_text_file import rows_from_text_file


# subdivx. El retorno tiene el formato:
# [["titulo1", "descripcion1", "url1"], ["titulo2", "descripcion2", "url2"] ... ]
def subdivx(search_words):
    url_base = "https://subdivx.com"
    url_token = f"{url_base}/inc/gt.php?gt=1"
    url_queries = f"{url_base}/inc/ajax.php"

    session = Session()
    token_request = session.get(url_token, timeout=5)

    if token_request.status_code != 200:
        return []

    payload = {
        'tabla': 'resultados',
        'filtros': '',
        'buscar396c': search_words,
        'token': token_request.json()['token']
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'es-419,es;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://subdivx.com',
        'priority': 'u=1, i',
        'referer': 'https://subdivx.com/',
        'sec-ch-ua': '"Not:A-Brand";v="24", "Chromium";v="134"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        "user-agent": sample(rows_from_text_file('user_agents.txt'), 1)[0],
        'x-requested-with': 'XMLHttpRequest',
    }

    search_request = session.post(url_queries, headers=headers, data=payload, timeout=5)

    if search_request.status_code != 200:
        return []

    try:
        return [[
            sub['titulo'],
            sub['descripcion'],
            f"https://subdivx.com/descargar.php?id={sub['id']}"
        ] for sub in search_request.json()['aaData']]
    except:
        # This must to be refactored to register logs
        return []

