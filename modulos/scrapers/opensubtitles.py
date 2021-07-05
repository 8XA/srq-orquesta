#!/bin/env python

#Recibe una lista de palabras de busqueda y retorna una
#lista con los subtitulos encontrados en la página de
#opensubtitles. El retorno tiene el formato:
#[["titulo1", "descripcion1", "url1"], ["titulo2", "descripcion2", "url2"] ... ]

import os
from modulos.caracteres_raros import  corregir

#Determina si la palabra es in indicador de una serie
#Ejemplo: S01E01
def serie(palabra):
    palabra_min = palabra.lower()

    #Condiciones para admitirlo como temporada/episodio
    if all(
            [
                #Tiene solo caracteres admitidos
                len([c for c in palabra_min if c in "se0123456789"]) == len(palabra_min),

                #Tiene las dos letras y estas no se repiten
                (len([c for c in palabra_min if c in "se"]) == 2) and (palabra_min.count("s") == 1),

                #La inicial es una letra
                palabra_min[0] in "se",

                #Tiene mas de 3 caracteres y el segundo no es una letra
                (len(palabra_min) > 3) and (palabra_min[1] not in "se"),

                #El ultimo caracter no es una letra
                palabra_min[-1] not in "se"
            ]
            ):

        #Separa el episodio y la temporada y los retorna en una lista
        letra_0 = palabra_min[0]
        letra_1 = [c for c in palabra_min[1:] if c in "se"][0]
        posicion_divisora = palabra_min.index(letra_1)

        temp_cap = {
                letra_0:palabra_min[1:posicion_divisora],
                letra_1:palabra_min[posicion_divisora + 1:]
                }

        #Retorna [temporada, capítulo]
        return [int(temp_cap["s"]), int(temp_cap["e"])]

    else:
        return False


###############################################

#Scraper
def opensubtitles(palabras):
    try:
        #Determina si es una serie
        episodio = [palabra for palabra in palabras if serie(palabra) != False]

        temp, cap = "", ""
        if len(episodio) > 0:
            temp_cap = serie(episodio[0])
            temp = "season-" + str(temp_cap[0]) + "/"
            cap = "episode-" + str(temp_cap[1]) + "/" 

        #Si es una serie, elimina las palabras relativas al episodio
        #(ejemplo: s01e01) y las pasa como parametro
        palabras_busqueda = [palabra for palabra in palabras if palabra not in episodio]
        
        pagina, subs = 0, []
        while (pagina == 0) or (len(txtBusqueda) > 1000):

            #Curl con headers
            #curl = "curl -H 'authority: 25748s.ha.azioncdn.net' -H 'sec-ch-ua: " + '"Chromium";v="91", " Not;A Brand";v="99"' + "' -H 'sec-ch-ua-mobile: ?0' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36' -H 'accept: */*' -H 'origin: https://www.opensubtitles.org' -H 'sec-fetch-site: cross-site' -H 'sec-fetch-mode: cors' -H 'sec-fetch-dest: empty' -H 'referer: https://www.opensubtitles.org/' -H 'accept-language: es-ES,es;q=0.9' --compressed "
            #Curl sencilla
            curl = "curl "
            linkBusqueda = "https://www.opensubtitles.org/es/search/sublanguageid-spa,spl/" + temp + cap + "moviename-" + "+".join(palabras_busqueda) + "/offset-" + str(pagina*40)
            txtBusqueda = os.popen(curl + "'" + linkBusqueda + "' | iconv -f iso-8859-1 -t utf-8").read()
            
            #Sección para pruebas
            with open("prueba","w") as documento:
                documento.write(linkBusqueda)
                #documento.write(txtBusqueda)

            renglones = txtBusqueda.split("\n")
            indices = [x for x in range(len(renglones)) if " - Ver En l" in renglones[x]]

            for indice in indices:
                #Determinando enlace del subtítulo
                enlace_0 = renglones[indice+1].index("href=") + 6
                enlace_1 = renglones[indice+1].index("onclick") - 2
                enlace = "https://www.opensubtitles.org" + renglones[indice+1][enlace_0:enlace_1]

                #Si la descripcion aparece completa
                if renglones[indice][0] == "(":
                    indexador_0, indexador_1, corrector = "<br />", "<br /><a", 6
                    desfase_t, desfase_a, desfase_d = 1, 0, 0
                #Si la descripción aparece incompleta
                else:
                    indexador_0, indexador_1, corrector = "<span title=", '">', 13
                    desfase_a, desfase_d = 0, 0
                    while renglones[indice - desfase_a][0] != "(":
                        desfase_a += 1

                    desfase_t = desfase_a + 1
                    
                    while "<span title=" not in renglones[indice - desfase_d]:
                        desfase_d += 1

                #Determinando título del subtítulo
                titulo_1_des = [x for x in renglones[indice-desfase_t]]
                titulo_1_des.reverse()
                titulo_0 = "".join(titulo_1_des).index('>""=')
                titulo = titulo_1_des[:titulo_0]
                titulo.reverse()
                titulo = "".join(titulo)
                
                #Determina el año
                year_0 = renglones[indice-desfase_a].index("</a")
                year = renglones[indice-desfase_a][:year_0]

                #Título completo
                fulltitle = corregir(titulo + " " + year)

                #Determinando descripción del subtítulo
                if (renglones[indice][0] == "(") or (renglones[indice-desfase_d][-3:] == "..."):
                    descripcion_0 = renglones[indice-desfase_d].index(indexador_0) + corrector
                    descripcion_1 = renglones[indice-desfase_d][descripcion_0:].index(indexador_1)
                    descripcion = corregir(renglones[indice-desfase_d][descripcion_0:descripcion_1 + descripcion_0])
                elif renglones[indice][0] not in "(<":
                    descripcion = corregir(renglones[indice-1] + " " + renglones[indice][:renglones[indice].index("<br /><a")])
                else:
                    descripcion = ""

                subs.append([fulltitle, descripcion, enlace])

            pagina += 1

        return subs

    except:
        return []
