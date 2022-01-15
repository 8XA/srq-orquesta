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


    #####################################################################################################
    #Animation:

    #Opening ascii art files
    files_route = '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/ascii_animations/cinema/'
    subs_list = file_list('subs_', [1,4])
    choosen_sub = subs_list[randint(1, len(subs_list) -1)]
    ascii_files_seq = file_list('dirt_', [1,5]) + subs_list + file_list('guy_', [1,2])
    ascii_files = ['eyes','mouth','curtains','light_base','shadows_base','srq'] + ascii_files_seq

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
    sub_flag = 0
    guy_number_str = str(randint(1,2))
    while True:

        message_color = color_dict['dark_on_dark']
        if counter%9 in range(0,5):
            message_color = color_dict['white_on_dark']

        #Print message
        message_win.addstr(0, 0, message[:cols_num -2], message_color | curses.A_BOLD)

        #Base printing
        layer_print('light_base', 'blue', ['#','@','='])
        layer_print('shadows_base', 'dark_blue', ['#','@','='])
        layer_print('light_base', 'default', ['/','\\','|','-','_', 'I'])
        layer_print('curtains', 'red', ['|','-','_','.',"'",'¨','´'])
        layer_print('srq', 'white_on_red', ['S','R','Q','_','|'])
        
        flash_off = randint(0,50)
        dirt_on = randint(0,5)
        dirt_color = 'dark_on_white'
        if dirt_on != 0:
            dirt_color = 'white_on_white'
        screen_color = 'white_on_white'
        if flash_off == 0:
            layer_print('light_base', 'dark_blue', ['#','@','='])
            dirt_color = 'white_on_dark'
            screen_color = 'dark_on_dark'
        
        #Screen with dirt
        screen_dirt = 'dirt_' + str(randint(1,5))
        layer_print(screen_dirt, dirt_color, ['-','~','"',',','{','}','S', '´'])
        layer_print(screen_dirt, screen_color, ['0'])

        #Screen number
        circuit = False

        mouth_offset = {
                '1':0,
                '2':13
            }
        eyes_offset = {
                '1':0,
                '2':11
            }

        #guys
        if counter%20 == 1:
            guy_number_str= str(randint(1,2))
            choosen_sub = [sub for sub in subs_list if sub != choosen_sub][randint(0,2)]
            sub_flag = 0
        if flash_off != 0:
            layer_print('guy_' + guy_number_str, 'dark_on_white', \
                    ['_','8','─','|','O','(',')','-','7','<','^','/','\\','¨','*','T','0'])

            #mouth
            if counter%2 == 1 and sub_flag > 2:
                layer_print('mouth', 'dark_on_white', ['O'], hor_offset=mouth_offset[guy_number_str])

            #subs
            if sub_flag > 4:
                layer_print(choosen_sub, 'white_on_dark', ['b','l','a','?','!','¡'])
                layer_print(choosen_sub, 'dark_on_dark', ['.'])
            sub_flag+=1
        
        #eyes
            if counter%20 == 10:
                layer_print('eyes','dark_on_white',['─'], hor_offset=eyes_offset[guy_number_str])

        counter+=1

        animation_win.box()
        animation_win.refresh()
        message_win.refresh()

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

def file_list(name:str, num:list):
    return [str(name) + str(x) for x in range(num[0], num[1] + 1)]
