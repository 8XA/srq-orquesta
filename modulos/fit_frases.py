#!/bin/env python

#Ingresa una frase y retorna la misma frase ajustada al ancho de pantalla

def fit_frase(numcols, msj):
    
    msj_lista = msj.split(" ")
    frase = ""
    longitud = 0

    for palabra in msj_lista:
        if len(palabra) > numcols:
            frase = frase + "\n" + palabra + " "

        elif longitud + len(palabra) < numcols:
            longitud = longitud + len(palabra) + 1
            frase = frase + palabra + " "
        else:
            longitud = len(palabra) + 1
            frase = frase + "\n" + palabra + " "

    return frase


#Centra el resultado de la función anterior
def fit_frase_centrada(numcols, msj):
    lista = [x for x in fit_frase(numcols, msj).split("\n") if x != ""]
    #print(lista)
    
    for indice in range(len(lista)):
        #print(indice)
        #input()
        if lista[indice][-1] == " ":
            lista[indice] = lista[indice][:-1]
        lista[indice] = ((numcols - len(lista[indice]))//2) * " " + lista[indice]

    return "\n".join(lista)


