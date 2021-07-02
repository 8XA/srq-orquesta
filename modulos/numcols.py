#!/bin/env python

#Limpia la pantalla y retorna el número de columnas

import curses, os

def num_cols():
    screen = curses.initscr() 
    num_cols = screen.getmaxyx()[1]
    curses.endwin()
    os.system("stty sane && clear")
    return num_cols
