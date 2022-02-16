#!/bin/env python

def is_filtered(sentence:str, plus_filter:list=[], minus_filter:list=[]):
    """
    Gets a sentence and their filters.
    It returns True if the sentence can be filtered.
    """
    
    if (len([filter_ for filter_ in plus_filter if filter_.lower() in \
            sentence.lower()]) == len(plus_filter) and len([filter_ for \
            filter_ in minus_filter if filter_[1:].lower() in sentence.lower()]) == 0):

        return True
    return False


def ordered_filters(filter_:str):
    """
    It get a filter string and separates it by commas and spaces.
    """

    filters = [valid_filter for valid_filter in " ".join(filter_.split(",")).split(" ") if valid_filter != '']

    minus_filter = []
    plus_filter = []

    for filter_ in filters:
        if len(filter_) > 1 and filter_[0] == '-':
            minus_filter.append(filter_)
        else:
            plus_filter.append(filter_)

    return plus_filter, minus_filter
    
