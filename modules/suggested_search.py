#!/bin/env python


from requests import get
from urllib.parse import quote


def suggested_search(search):
    url = "https://suggestqueries.google.com/complete/search"

    params = {
        "client": "firefox",
        "q": quote(search),
        "hl": "es"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    response = get(url, params=params, headers=headers)
    if response.status_code == 200 and len(response.json()[1]) > 0:
        return response.json()[1][0]
    else:
        return search
