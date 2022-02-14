#!/bin/env python

#Recibe una lista de palabras de busqueda y retorna una
#lista con los subtitulos encontrados en la página de
#opensubtitles. El retorno tiene el formato:
#[["titulo1", "descripcion1", "url1"], ["titulo2", "descripcion2", "url2"] ... ]

import os
from requests import get, Session
from modules.user_agents import user_agents
from requests.exceptions import RequestException
from urllib.parse import quote

def opensubtitles(palabras):
    try:
        palabras_busqueda = [quote(palabra) for palabra in palabras]
        agents = user_agents()
        
        pagina, subs = 0, []
        to_iterate = True
        #Solo descargará la primera página para evitar bloqueo
        while to_iterate:

            linkBusqueda = "https://www.opensubtitles.org/es/search/sublanguageid-spa,spl/" + \
                    "moviename-" + "+".join(palabras_busqueda) + "/offset-" + str(pagina*40)
            try:
                header = {"User-Agent": agents[pagina]}
                browser_session = Session()
                txtBusqueda = browser_session.get(linkBusqueda, timeout=7, headers=header).text
                browser_session.close()
            except RequestException as e:
                txtBusqueda = ''

            renglones = txtBusqueda.split("\n")
            indices = [x for x in range(len(renglones)) if " - Ver En l" in renglones[x]]

            page_subs = []
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
                titulo_0 = "".join(titulo_1_des).index('>"')
                titulo = titulo_1_des[:titulo_0]
                titulo.reverse()
                titulo = "".join(titulo)
                
                #Determina el año
                year_0 = renglones[indice-desfase_a].index("</a")
                year = renglones[indice-desfase_a][:year_0]

                #Título completo
                fulltitle = titulo + " " + year

                #Determinando descripción del subtítulo
                if (renglones[indice][0] == "(") or (renglones[indice-desfase_d][-3:] == "..."):
                    descripcion_0 = renglones[indice-desfase_d].index(indexador_0) + corrector
                    descripcion_1 = renglones[indice-desfase_d][descripcion_0:].index(indexador_1)
                    descripcion = renglones[indice-desfase_d][descripcion_0:descripcion_1 + descripcion_0]
                elif renglones[indice][0] not in "(<":
                    descripcion = renglones[indice-1] + " " + \
                            renglones[indice][:renglones[indice].index("<br /><a")]
                else:
                    descripcion = ""

                page_subs.append([fulltitle, descripcion, enlace])
            subs += page_subs
            to_iterate = len(page_subs) > 0

            pagina += 1

        return subs

    except:
        return []
