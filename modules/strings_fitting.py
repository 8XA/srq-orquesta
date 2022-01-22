#!/bin/env python

from termcolor import colored

def phrase_fitting(cols_number, message, tags=False):
    """
    It gets a message to fit in a screen with certain columns number (cols_number).
    With tags=True, this function ingrores the :x: tags.
    It returns a string with "\n" character as a separator.
    """
    words = message.split(' ')
    final_string = ""
    row = ""
    row_lenght = 0

    if tags:
        words_lenght = [len(word) - ((word.count("<g>") + word.count("<b>") + \
                word.count("<r>") + word.count("<a>") + word.count("<R>") + \
                word.count("<c>") + word.count("<B>")) * 3) for word in words]
    else:
        words_lenght = [len(word) for word in words]

    for indx in range(len(words_lenght)):
        if (row_lenght == 0) or (row_lenght + words_lenght[indx] < cols_number):
            row += words[indx] + " "
            row_lenght += words_lenght[indx] + 1
        else:
            if words_lenght[indx] >= cols_number:
                final_string += (row + "\n" + words[indx] + "\n")
                row_lenght = 0
            else:
                final_string += (row + "\n")
                row = words[indx] + " "
                row_lenght = words_lenght[indx] + 1
    final_string += row
    
    return final_string


#Centra el resultado de la función anterior
def centered_phrase_fitting(numcols, msj, tags=None):
    lista = [x for x in phrase_fitting(numcols, msj).split("\n") if x != ""]
    
    for indice in range(len(lista)):
        if lista[indice][-1] == " ":
            lista[indice] = lista[indice][:-1]
        lista[indice] = ((numcols - len(lista[indice]))//2) * " " + lista[indice]

    return "\n".join(lista)


def colored_centered_filter(columns_number, phrase, color:str='white', background:str='on_red'):
    """
    Enter a filter as a string and get it centered and colored
    """
    centered_phrase = centered_phrase_fitting(columns_number, phrase)
    colored_list = list(centered_phrase)

    for x in range(len(colored_list)):
        if colored_list[x] not in [' ', '\n']:
           colored_list[x] = colored(colored_list[x], color, background, attrs=['bold','dark'])

    return "".join(colored_list)


