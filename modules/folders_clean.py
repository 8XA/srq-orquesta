#!/bin/env python

from modules.admin_db import read_simple_list, edit_simple_list
from subprocess import Popen, PIPE
from pathlib import Path

def subs_and_folders_deletion():
    """
    It verifies the list of downloaded subs:
        If the subtitle video does'nt exist, then deletes the subtitle.
        If this function deletes the subtitle and there is no other file in the folder, the folder is deleted.
    
    It takes no parameters and returns nothing.
   """ 
    registered_subs = read_simple_list('downloaded_subtitles')
    
    for sub in registered_subs:
        
        files_route = sub[:sub.rindex('/')] + "/"
        files_name = sub[:sub.rindex('.')][len(files_route):] + ".*"

        if files_number(files_route, files_name) <= 1:
            if Path(sub).is_file():
                deletion = Popen(["rm", "-f", sub], stderr=PIPE, stdout=PIPE)
            if files_number(files_route, all_files=True) == 1:
                deletion = Popen(["rm", "-rf", files_route], stderr=PIPE, stdout=PIPE)


def files_number(files_route:str, files_name:str=None, all_files:bool=False):
    """
    It returns the number of files in certain route:
        - With x name
        - All the files
    """
    base_command = ["find", files_route]
    command_dict = {
            True:['*'],
            False:["-type", "f", "-iname", files_name]
        }
    
    files_list = Popen(base_command + command_dict[all_files], stdout=PIPE, stderr=PIPE)

    raw_files = str(files_list.stdout.read())
    splitted_files = raw_files.split('\\n')
    files_number = len(splitted_files) -1
    
    return files_number

