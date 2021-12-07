#!/bin/env python

#Recibe un enlace de descarga. Con él, 
#retorna el enlace directo y el ID de archivo

import os

def get_enlace(enlace_de_lista):
    #Descargando html
    txtPagina = os.popen("curl '" + enlace_de_lista + "' \
            | iconv -f iso-8859-1 -t utf-8").read()
    
    #Scraping
    index_1 = txtPagina.index('"link1"')
    index_2 = txtPagina[index_1:].index('">')
    id_sub = txtPagina[index_1 + 14 : index_1 + index_2]
    
    #Generando link de descarga
    link = "https://www.subdivx.com/" + id_sub

    return link
