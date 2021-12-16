#!/bin/env python

def corregir(texto_original):

    texto = "".join(texto_original.split("Â"))
    texto = " ".join(texto.split("\n"))
    texto = "ñ".join(texto.split("Ã±"))
    texto = "Ñ".join(texto.split("Ã\x91"))
    texto = "á".join(texto.split("Ã¡"))
    texto = "Á".join(texto.split("Ã\x81"))
    texto = "é".join(texto.split("Ã©"))
    texto = "É".join(texto.split("Ã\x89"))
    texto = "í".join(texto.split("Ã\xad"))
    texto = "Í".join(texto.split("Ã\x8d"))
    texto = "ó".join(texto.split("Ã³"))
    texto = "Ó".join(texto.split("Ã\x93"))
    texto = "ú".join(texto.split("Ãº"))
    texto = "Ú".join(texto.split("Ã\x9a"))
    texto = "'".join(texto.split("â\x80\x99"))

    return texto
