#!/bin/env python

from termcolor import colored

#Ingresa una frase y retorna la misma frase ajustada al ancho de pantalla

def phrase_fitting(numcols, msj):
    
    msj_lista = msj.split(" ")
    frase = ""
    longitud = 0

    for palabra in msj_lista:
        if len(palabra) > numcols:
            frase = frase + "\n" + palabra + " "

        elif longitud + len(palabra) <= numcols:
            longitud = longitud + len(palabra)
            frase = frase + palabra
            if longitud < numcols:
                longitud += 1
                frase += " "
        else:
            longitud = len(palabra) + 1
            frase = frase + "\n" + palabra + " "

    return frase


#Centra el resultado de la función anterior
def centered_phrase_fitting(numcols, msj):
    lista = [x for x in phrase_fitting(numcols, msj).split("\n") if x != ""]
    #print(lista)
    
    for indice in range(len(lista)):
        #print(indice)
        #input()
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


