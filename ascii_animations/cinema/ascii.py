#!/bin/env python

import curses
from time import sleep
from os import system
from random import randint
from modules.admin_db import read_settings, edit_settings

def ascii_animation(message, scraper_num):
    global layer_dict, color_dict, animation_win
    edit_settings("run_animation", "0")

    screen = curses.initscr()

    #Invisible cursor
    curses.curs_set(0)
    
    #Enable colors
    curses.start_color()

    #Availiable colors
        #blue
    curses.init_pair(1, 19, 0)
        #dark_blue
    curses.init_pair(2, 17, 0)
        #red
    curses.init_pair(3, 124, 0)
        #white_on_white
    curses.init_pair(4, 255, 255)
        #white_on_dark
    curses.init_pair(5, 255, 16)
        #dark_on_white
    curses.init_pair(6, 16, 255)
        #dark_on_dark
    curses.init_pair(7, 16, 16)
        #gray_on_gray
    curses.init_pair(8, 243, 243)
        #white_on_red
    curses.init_pair(9, 255, 124)

    #screen dimentions
    rows_num = screen.getmaxyx()[0]
    cols_num = screen.getmaxyx()[1]

    message_win = curses.newwin(1, cols_num, 0, 0)
    animation_win = curses.newwin(rows_num - 1, cols_num, 1, 0)
    #message_win = curses.newwin(1, cols_num, rows_num-1, 0)

    #Print message
    message_win.addstr(0, 0, message[:cols_num -2])
    message_win.refresh()
        

    #####################################################################################################
    #Animation:

    #Opening ascii art files
    files_route = '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/ascii_animations/cinema/'
    ascii_files = ['1','2','3','curtains','light_base','shadows_base','dirt_1','dirt_2','dirt_3','dirt_4','dirt_5','srq']

    #The curtain center file was taken as the refference
    draw_center = 39
    max_vertical_draw = 27
    win_center = cols_num//2
    hor_cut = draw_center - win_center
    #row nums without borders and message row
    ver_lenght = rows_num - 3

    layer_dict = {}
    for filename in ascii_files:
        with open(files_route + filename, "r") as file:
            layer_dict[filename] = file.readlines()
            
            #Vertical fitting
            if max_vertical_draw > ver_lenght:
                layer_dict[filename] = layer_dict[filename][2: ver_lenght + 2]

            #Horizontal fitting
            for idx in range(len(layer_dict[filename])):
                if hor_cut > 0:
                    layer_dict[filename][idx] = layer_dict[filename][idx][hor_cut:hor_cut + (cols_num -1)]
                elif hor_cut < 0:
                    layer_dict[filename][idx] = (abs(hor_cut) * " " + layer_dict[filename][idx])[:cols_num -1 -abs(hor_cut)]

    #Colors
    color_dict = {
            'default':curses.color_pair(0),
            'blue':curses.color_pair(1),
            'dark_blue':curses.color_pair(2),
            'red':curses.color_pair(3),
            'white_on_white':curses.color_pair(4),
            'white_on_dark':curses.color_pair(5),
            'dark_on_white':curses.color_pair(6),
            'dark_on_dark':curses.color_pair(7),
            'gray':curses.color_pair(8),
            'white_on_red':curses.color_pair(9)
        }

    counter = 0
    screen_number = 3
    while True:
        #Base printing
        layer_print('light_base', 'blue', ['#','@'])
        layer_print('shadows_base', 'dark_blue', ['#','@','='])
        layer_print('light_base', 'default', ['/','\\','|','-','_', 'I'])
        layer_print('curtains', 'red', ['|','-','_','.',"'",'¨','´'])
        layer_print('srq', 'white_on_red', ['S','R','Q','_','|'])
        
        flash_off = randint(0,9)
        dirt_on = randint(0,5)
        dirt_color = 'dark_on_white'
        if dirt_on != 0:
            dirt_color = 'white_on_white'
        screen_color = 'white_on_white'
        if flash_off == 0:
            layer_print('light_base', 'dark_blue', ['#','@'])
            dirt_color = 'white_on_dark'
            screen_color = 'dark_on_dark'
        
        #Screen with dirt
        screen_dirt = 'dirt_' + str(randint(1,5))
        layer_print(screen_dirt, dirt_color, ['-','~','"',',','{','}','S', '´'])
        layer_print(screen_dirt, screen_color, ['0'])

        #Screen number
        circuit = False
        if counter == 10:
            counter = 0
            screen_number -= 1
            if screen_number == 0:
                circuit = True
                screen_number = 3
        
        #Print number and their background
        hor_offset = 0
        vert_offset = 0
        if counter//2 == counter/2 and randint(0,5) == 0:
            hor_offset = randint(-1,1)
            vert_offset = randint(-1,1)
        layer_print(str(screen_number), 'dark_on_dark', ['O'], hor_offset, vert_offset)
        layer_print(str(screen_number), 'gray', ['.'], hor_offset, vert_offset)

        counter+=1

        #Delay with dark screen
        if circuit == True:
            for x in range(20): 

                dirt_on = randint(0,5)
                dirt_color = 'dark_on_dark'
                if dirt_on == 0:
                    dirt_color = 'white_on_dark'
                else:
                    previous_screen_dirt = screen_dirt
                    while screen_dirt == previous_screen_dirt:
                        screen_dirt = 'dirt_' + str(randint(1,5))
                layer_print(screen_dirt, 'dark_on_dark', ['0','-','~','"',',','{','}','S', '´'])
                layer_print(screen_dirt, dirt_color, ['-','~','"',',','{','}','S', '´'])
                layer_print('light_base', 'dark_blue', ['#','@'])
                animation_win.refresh()

                if read_settings("run_animation") - scraper_num == 0:
                    break
                sleep(0.1)

        animation_win.box()
        animation_win.refresh()

        if read_settings("run_animation") - scraper_num == 0:
            break
        sleep(0.1)

    screen.clear()
    curses.endwin()
    system("stty sane && clear")
    edit_settings("run_animation", "0")


def layer_print(
        layer:str,
        color:str,
        chars:list,
        hor_offset:int=0,
        vert_offset:int=0
    ):
    
    global layer_dict, color_dict, animation_win

    for y in range(len(layer_dict[layer])):
        for x in range(len(layer_dict[layer][y][:-1])):
            ch = layer_dict[layer][y][x]
            if ch in chars:
                animation_win.addch(y + 1 + vert_offset, x + 1 + hor_offset, \
                        ch, color_dict[color] | curses.A_BOLD)


