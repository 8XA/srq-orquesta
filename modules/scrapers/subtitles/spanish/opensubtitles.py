#!/bin/env python


from concurrent.futures import ThreadPoolExecutor, as_completed
from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import quote
from random import shuffle
from itertools import cycle

from modules.rows_from_text_file import rows_from_text_file


def opensubtitles(search_words):
    """
    This function take a sentence string as a parameter and returns a list of
    subtitles from opensubtitles with the following format:

    [["title1", "description1", "url1"], ["title2", "description2", "url2"] ... ]
    """

    last_page = 0
    agent = user_agent_generator()
    scraping_lead = opensubtitles_onepage(search_words, last_page, next(agent))
    MAX_SUBTITLES = 1000 # maximum quantity of subtitles to return

    complete_subs_list = scraping_lead['subs_list']
    executor = ThreadPoolExecutor(max_workers=5)
    threads = dict()

    while (not scraping_lead['pagination_done'] or len(threads) != last_page) and last_page < (MAX_SUBTITLES/40):
        for page in range(last_page + 1, scraping_lead['last_page']):
            threads[page] = executor.submit(opensubtitles_onepage, search_words, page, next(agent))

            if page == scraping_lead['last_page'] - 1:
                scraping_lead = threads[page].result()
                last_page = page

    for thread in as_completed(threads.values()):
        complete_subs_list += thread.result()['subs_list']

    executor.shutdown(wait=True)

    return complete_subs_list


def opensubtitles_onepage(search_words, page, headers):
    results = {
        "subs_list": [],
        "last_page": page,
        "pagination_done": True
    }

    moviename = quote('+'.join(search_words.strip().split()))
    url = (
        f"https://www.opensubtitles.org/es/search/moviename-{moviename}"
        f"/sublanguageid-spa,spl/offset-{page * 40}"
    )

    session = Session()
    request = session.get(url, headers=headers)

    if request.status_code != 200:
        return results

    soup = BeautifulSoup(str(request.text), "lxml")
    raw_subs = soup.body.find_all(
        'tr',
        class_=lambda class_name: (
            class_name and 'change' in class_name and 'expandable' in class_name
        )
    )

    for raw_sub in raw_subs:
        raw_description = str(raw_sub)

        idx_1 = raw_description.find('<br/>')
        idx_2 = raw_description[idx_1 + 5:].find('<br/>')
        description = raw_description[idx_1 + 5:idx_1 + idx_2 + 5].strip()

        if '<span title="' in description:
            idx_1 = description.find('<span title="')
            idx_2 = description[idx_1 + 13:].find('">')

            description = f"{description[:idx_1]}{description[idx_1 + 13:idx_1 + 13 + idx_2]}"
            description = description.replace("\n", "\t").split("\t")
            description = '\n'.join([element for element in description if element != ''])

        results['subs_list'].append([
            raw_sub.find('a', class_='bnone')['title'][13:],
            description,
            f"https://dl.opensubtitles.org/en/download/sub/{raw_sub['id'][4:]}"
        ])

    pager = soup.find(id="pager")
    if pager is None:
        return results

    pager = pager.find_all('a')
    if len(pager) > 1:
        if pager[-1].get_text() == '>>':
            results['pagination_done'] = False
            results['last_page'] = int(pager[-2].get_text())
        else:
            results['last_page'] = int(pager[-1].get_text())

    return results


def user_agent_generator():
    agents = rows_from_text_file('user_agents.txt')
    shuffle(agents)

    for agent in cycle(agents):
        yield {"User-Agent": agent}
