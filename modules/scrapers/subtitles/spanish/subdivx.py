#!/bin/env python

#Recibe una lista de palabras de busqueda y retorna una
#lista con los subtitulos encontrados en la página de
#subdivx. El retorno tiene el formato:
#[["titulo1", "descripcion1", "url1"], ["titulo2", "descripcion2", "url2"] ... ]

import os
from requests import get
from urllib.parse import quote

def subdivx(palabras):
    try:
        subs, subspag, pagina = [], [], 0
        while subspag != [] or pagina == 0:
            pagina+=1

            search = []
            for word in palabras:
                search.append(quote(word))
            suma = "+".join(search)

            #Obtiene el html del link con las palabras de búsqueda
            linkBusqueda = "https://www.subdivx.com/index.php?buscar2=" + suma + "&accion=5&masdesc=&subtitulos=1&realiza_b=1=&pg=" + str(pagina)
            txtBusqueda = get(linkBusqueda, timeout=5).text

            #Extrae la información del html descargado
            x = 0
            subspag = []
            while '"titulo_menu_izq" href="' in txtBusqueda[x:]:
                ind = txtBusqueda[x:].index('"titulo_menu_izq" href="')
                ind2 = txtBusqueda[x+ind:].index('">')
                ind3 = txtBusqueda[x+ind+ind2:].index('</a>')

                #Título
                enlace = txtBusqueda[24+x+ind:x+ind+ind2]
                titulo = txtBusqueda[x+ind+ind2+2:x+ind+ind2+ind3]
                
                #Descripción
                x += (ind+ind2+ind3)
                ind4 = txtBusqueda[x:].index('<div id="buscador_detalle_sub"')
                ind5 = txtBusqueda[x+ind4:].index('</div>')
                descripcion = txtBusqueda[31+x+ind4:x+ind4+ind5]

                subspag.append([titulo, descripcion, enlace])

                x += (ind4+ind5)

            subs += subspag
        return subs

    except:
        return []
