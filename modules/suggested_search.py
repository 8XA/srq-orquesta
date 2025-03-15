#!/bin/env python


from requests import Session
from bs4 import BeautifulSoup
from random import sample
from urllib.parse import quote

from modules.rows_from_text_file import rows_from_text_file


def suggested_search(search):

    headers = {
        "User-Agent": sample(rows_from_text_file('user_agents.txt'), 1)[0]
    }

    url = f"https://mx.search.yahoo.com/search?p={quote(search)}"

    s = Session()
    r = s.get(url, headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(str(r.text), "lxml")
        a_tags = soup.find_all('a', class_='fc-denim')
        if len(a_tags) == 2:
            return a_tags[0].get_text()

    return search
