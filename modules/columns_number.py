#!/bin/env python

from curses import initscr, endwin
from os import system

def columns_number_func():

    """DESCRIPTION:
        - This function cleans the screen and returns the current columns number.

    HOW TO USE:
        - call columns_number_func().
    """

    screen = initscr() 
    columns_number = screen.getmaxyx()[1]
    endwin()

    system("stty sane && clear")

    return columns_number
