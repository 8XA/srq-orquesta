#!/bin/env python

#Recibe una lista de palabras de busqueda y retorna una
#lista con los subtitulos encontrados en la página de
#opensubtitles. El retorno tiene el formato:
#[["titulo1", "descripcion1", "url1"], ["titulo2", "descripcion2", "url2"] ... ]

import os

#Determina si la palabra es in indicador de una serie
#Ejemplo: S01E01
def serie(palabra):
    palabra_min = palabra.lower()
    caracteres = "se0123456789"

    #Condiciones para admitirlo como temporada/episodio
    if all(
            [
                #Tiene solo caracteres admitidos
                len([c for c in palabra_min if c in caracteres]) == len(palabra_min),

                #Tiene solo una S y es el primer caracter
                (palabra_min[0] == "s") and (palabra_min.count("s") == 1),

                #Tiene solo una E y no es el ultimo caracter
                (palabra_min[-1] != "e") and (palabra_min.count("e") == 1),

                #Hay un número despues de cada letra
                (len(palabra_min) > 3) and (palabra_min[1] != "e")
            ]
            ):

        #Separa el episodio y la temporada y los retorna en una lista
        separacion = palabra_min.split("e")
        return [int(separacion[0][1:]), int(separacion[1])]

    else:
        return False


def opensubtitles(palabras):
    #Determina si es una serie
    episodio = [palabra for palabra in palabras if serie(palabra) != False]

    temp, cap = "", ""
    if len(episodio) > 0:
        temp_cap = serie(episodio[0])
        temp = "season-" + str(temp_cap[0]) + "/", 
        cap = "episode-" + str(temp_cap[1]) + "/", 

    #Si es una serie, elimina las palabras relativas al episodio
    #(ejemplo: s01e01) y las pasa como parametro
    palabras_busqueda = [palabra for palabra in palabras if palabra not in episodio]
    
    pagina = 0

#    lista = []
#    txtBusqueda, pagina = "", 0
#    while (pagina == 0) or (len(txtBusqueda) > 500):
#        linkBusqueda = "https://www.opensubtitles.org/es/search/sublanguageid-spa,spl/" + temp + cap + "moviename-" + "+".join(palabras_busqueda) + "/offset-" + str(pagina*40)
#        txtBusqueda = os.popen("curl '" + linkBusqueda + "' | iconv -f iso-8859-1 -t utf-8").read()
#        lista.append(txtBusqueda)
#        with open("scrap" + str(pagina), "w") as docu:
#            docu.write(txtBusqueda)
#        pagina += 1


    linkBusqueda = "https://www.opensubtitles.org/es/search/sublanguageid-spa,spl/" + temp + cap + "moviename-" + "+".join(palabras_busqueda) + "/offset-" + str(pagina*40)
    txtBusqueda = os.popen("curl '" + linkBusqueda + "' | iconv -f iso-8859-1 -t utf-8").read()

    renglones = txtBusqueda.split("\n")
    indices = [x for x in range(len(renglones)) if " - Ver En l" in renglones[x]]

    subs = []
    #return [renglones,indices]
    for indice in indices:
        #Determinando enlace del subtítulo
        enlace_0 = renglones[indice+1].index("href=") + 6
        enlace_1 = renglones[indice+1].index("onclick") - 2
        enlace = "https://www.opensubtitles.org" + renglones[indice+1][enlace_0:enlace_1]

        #Si la descripcion aparece completa
        if renglones[indice][0] == "(":
            desfase_r, desfase_ad = 1, 0
            indexador_0, indexador_1, corrector = "<br />", "<br /><a", 6
        #Si la descripción aparece incompleta
        else:
            desfase_r, desfase_ad = 2, 1
            indexador_0, indexador_1, corrector = "<span title=", '">', 13

        #Determinando título del subtítulo
        titulo_1_des = [x for x in renglones[indice-desfase_r]]
        titulo_1_des.reverse()
        titulo_0 = "".join(titulo_1_des).index('>""=')
        titulo = titulo_1_des[:titulo_0]
        titulo.reverse()
        titulo = "".join(titulo)
        
        #Determina el año
        year_0 = renglones[indice-desfase_ad].index("</a")
        year = renglones[indice-desfase_ad][:year_0]

        #Título completo
        fulltitle = titulo + " " + year

        #Determinando descripción del subtítulo
        descripcion_0 = renglones[indice-desfase_ad].index(indexador_0) + corrector
        descripcion_1 = renglones[indice-desfase_ad][descripcion_0:].index(indexador_1)
        descripcion = renglones[indice-desfase_ad][descripcion_0:descripcion_1 + descripcion_0]

        subs.append([fulltitle, descripcion, enlace])
    
    return subs
