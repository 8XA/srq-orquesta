#!/bin/env python

from subprocess import Popen, PIPE, call

def columns_number_func(side:str='cols', clean_screen:bool=True):
    """
    DESCRIPTION:
        - This function return the current sizo of a screen side.
            * Cleans the screen by default, but this is optional.

    HOW TO USE:
        - call columns_number_func() with the parameters as follows:
            side: 'lines' or 'cols'
            clean_screen: True or False

    RETURNS:
        'row' or 'cols': The integer value

    """

    if clean_screen:
        call("clear")

    side_command = Popen("tput " + side, shell=True, stderr=PIPE, stdout=PIPE)
    raw_side = str(side_command.stdout.read())
    side_size = int(raw_side[2:-3])

    return side_size
