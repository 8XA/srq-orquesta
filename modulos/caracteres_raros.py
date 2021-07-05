#!/bin/env python

def corregir(texto_original):

    texto = "".join(texto_original.split("Â"))
    texto = " ".join(texto.split("\n"))
    texto = "ñ".join(texto.split("Ã±"))
    texto = "Ñ".join(texto.split("Ã\x91"))
    texto = "á".join(texto.split("Ã¡"))
    texto = "é".join(texto.split("Ã©"))
    texto = "í".join(texto.split("Ã\xad"))
    texto = "ó".join(texto.split("Ã³"))
    texto = "ú".join(texto.split("Ãº"))
    texto = "'".join(texto.split("â\x80\x99"))
   
    return texto
