#!/bin/env python

from requests import get

def suggested_search(search):
    """
    It gets a sentence.
    It returns the suggested search by google.
    """

    words_sum = "+".join(search.split(" "))
    words_sum = words_sum.replace("'","%27")

    url = "https://www.google.com.mx/search?q=" + words_sum
    raw = get(url).text

    index_0 = raw.index('href="/search?q=')
    index_0 = raw[index_0 + 1:].index('href="/search?q=') + index_0 + 17
    index_1 = raw[index_0:].index('&amp;') + index_0

    raw_suggested = raw[index_0:index_1]
    suggested = " ".join(raw_suggested.split("+"))

    return suggested
