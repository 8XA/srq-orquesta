#!/bin/env python

def user_agents():
    """
    It retuns a list with user agents.
    """

    route = '/data/data/com.termux/files/usr/share/srq-orquesta/srq-orquesta/user_agents.txt'

    with open(route, "r") as file:
        raw_list = file.readlines()

    user_agent_list =  [user_agent[:-1] for user_agent in raw_list[:-1]]

    return user_agent_list
