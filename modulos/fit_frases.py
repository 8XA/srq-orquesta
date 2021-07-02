#!/bin/env python

#Ingresa una frase y retorna la misma frase ajustada al ancho de pantalla

def fit_frase(numcols, msj):
    
    msj_lista = msj.split(" ")
    frase = ""
    longitud = 0

    for palabra in msj_lista:
        if longitud + len(palabra) < numcols:
            longitud = longitud + len(palabra) + 1
            frase = frase + palabra + " "
        else:
            longitud = len(palabra) + 1
            frase = frase + "\n" + palabra + " "

    return frase
