#!/bin/env python

# This module ensures that external apps are able to be executed by Termux, like the video player
def allow_external_apps():

    termux_properties = "/data/data/com.termux/files/home/.termux/termux.properties"

    with open(termux_properties, "r+") as file:
        raw_lines = file.readlines()
        
        for idx in range(len(raw_lines)):
            if raw_lines[idx] == "# allow-external-apps = true\n":
                raw_lines[idx] = "allow-external-apps = true\n"

        file.seek(0)
        file.writelines(raw_lines)
        file.truncate
