#!/bin/env python

from subprocess import Popen, PIPE, call

def columns_number_func(side:str='cols', clean_screen:bool=True):
    """
    DESCRIPTION:
        - This function return the current sizo of a screen side.
            * Cleans the screen by default, but this is optional.

    HOW TO USE:
        - call columns_number_func() with the parameters as follows:
            side: 'rows' or 'cols'
            clean_screen: True or False
    """

    if clean_screen:
        call("clear")

    size_command = Popen(["stty","size"], stdout=PIPE, stderr=PIPE)
    raw_size = str(size_command.stdout.read())
    dimentions = raw_size[2:-3].split(" ")

    request = dimentions[1]
    if side == 'rows':
        request = dimentions[0]

    return int(request)



