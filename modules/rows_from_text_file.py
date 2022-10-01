#!/bin/env python

def rows_from_text_file(filename):
    """
    It retuns a list with the rows of a text file.
    """

    route = f"/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/{ filename }"

    with open(route, "r") as file:
        raw_list = file.readlines()

    rows_list =  [row[:-1] for row in raw_list[:-1]]

    return rows_list
