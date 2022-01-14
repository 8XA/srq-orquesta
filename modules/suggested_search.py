#!/bin/env python

from requests import get
from urllib.parse import unquote, quote
from os import system

def suggested_search(search):
    """
    It gets a sentence.
    It returns the suggested search by google.
    """

    separated_search = search.split(' ')
    for x in range(len(separated_search)):
        separated_search[x] = quote(separated_search[x])
    words_sum = '+'.join(separated_search)

    url = "https://www.google.com.mx/search?q=" + words_sum
    try:
        raw = get(url).text
    except RequestException as e:
        raw = ''

    index_0 = raw.index('href="/search?q=')
    index_0 = raw[index_0 + 1:].index('href="/search?q=') + index_0 + 17
    index_1 = raw[index_0:].index('&amp;') + index_0

    raw_suggested = raw[index_0:index_1]
    suggested = " ".join(raw_suggested.split("+"))
    suggested = unquote(suggested, encoding='utf-8', errors=' ')
    
    if len(suggested) == 0:
        return search
    return suggested
