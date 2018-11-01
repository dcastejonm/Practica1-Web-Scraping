#Importamos funciones

from urllib.request import urlopen

from bs4 import BeautifulSoup

import numpy as np

import pandas as pd

#Se define la primera función: Esta función busca todos los links de un html en
# base a unos parámetros de búsqueda.

def buscalinks(url, tag, atr, tex, dep = 1, tag2 = 1):
    html = urlopen(url)
    soup = BeautifulSoup(html.read(),"html5lib")

    if atr == "text":

        nav = soup.findAll(tag, text = tex)

    else:

        nav = soup.findAll(tag, {atr : tex})

    links = np.array([])

    if dep == 1:

        for lin in nav:

            link = lin['href']
            links = np.append(links, link)
            
    elif dep == 2:

        for lin in nav:

            link = lin.find(tag2)['href']
            links = np.append(links, link)

    if len(links) == 1:
            
        print ("Se ha encontrado un link en la búsqueda")

        return links[0]

    elif len(links) > 1:
           
        print ("Se ha encontrado más de un link en la búsqueda")
           
        return links



# Se define la segunda función: Busca un único link válido
# para unos parámetros de búsqueda. En caso de que encuentre más de uno,
# devuelve error.

def linkunico(links, sub):

    lind = np.array([])

    for link in links:
        if sub in link:
            r = 1
            lind = np.append(lind,r)
        else:
            r = 0
            lind = np.append(lind,r)
    
    if sum(lind) != 1:
        print ("Error, revisa los parámetros de búsqueda")

    else:

        lind = lind.tolist()
        ind = lind.index(1)

        return links[ind]

# Se define la tercera funcion. A partir del link del día de la consulta, genera
# los links para los datos de los días anteriores requeridos.

def linksgen(d,link, url):


    links = np.array([])

    for i in range (0,d):

        n = 7 - i
                        
        links = np.append(links,url + link.replace("x=d07","x=d0" + str(n)))
            
    return links

   
# Se define la cuarta función. Carga los csv, añadiendo una columna con la fecha
# Une todos los csv en un mismo dataframe.

def cargacsv(links):
    df = pd.DataFrame()
    lista = []

    for link in links:
            
        pf = pd.read_csv(link, skiprows = 3, encoding = 'latin-1')
        fecha = list(pd.read_csv(link,skiprows = 2, nrows = 0, encoding = 'latin-1'))[-1]
        pf['Fecha'] = fecha

        lista.append(pf)

    df = pd.concat(lista)

    print("Datos cargados en un DataFrame")

    return df


# Se define la quinta función. En los campos en que hay temperatura/viento y hora,
# separa la información.

def limphora (df, campos):

    pf = df[campos]

    for campo in campos:

        df[campo] = pf[campo].str.split('(').str[0]
        n = campo + "(hora)"
        df[n] = pf[campo].str.split('(').str[1].str.split(')').str[0]

    print('Variables separadas')
    return df

# Se define la sexta función. Extrae la información del html de la web.

def dathtml (links):

    lista = []

    i = 6
   
    for link in links:

        html = urlopen(link)
        soup = BeautifulSoup(html.read(),"html5lib")

        nav = soup.findAll("table", {"summary":"Últimos datos meteorológicos observados por cada ciudad de la comunidad autónoma seleccionada"})

        nav2 = soup.findAll("div", {'class':'boton'})

        nav2 = nav2[:int(len(nav2)/2)]

        fecha = nav2[i].get_text()

        fecha = fecha.strip()

        i = i-1

        lineas = nav[0].findAll("tbody")[0].findAll("tr")

        for linea in lineas:

            cols = linea.findAll("td")
            
            l = np.array([])

            for col in cols:

                l = np.append(l, col.text)

# La estructura del html tiene algunos valores repetidos, se corrige para que
# no estén repetidos.

            errors = [4,7,8,9,10,11]

            for error in errors:
                
                m = len(l[error])
                l[error] = l[error][:int(m/2)]
                           
            l= np.append(l,fecha)

            lista.append(l)

    df = pd.DataFrame(lista)

    cabeceras = nav[0].findAll("thead")[0].findAll("th")

    nombres = np.array([])

    for cabecera in cabeceras:

        nombres= np.append(nombres, cabecera['abbr'])  

    nombres= np.append(nombres, "Fecha")

    df.columns = nombres

    return df

            

        

        

    
