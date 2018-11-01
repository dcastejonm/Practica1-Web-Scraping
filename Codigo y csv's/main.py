from functions import buscalinks

from functions import linkunico

from functions import linksgen

from functions import cargacsv

from functions import limphora

from functions import dathtml

import time

# Definimos la url principal

url = "http://www.aemet.es"

#Se pide introducir el número de días que se quiere descargar.

d = int(input("¿De cuantos días deseas descargar información?\n(AEMET permite hasta los 7 días anteriores a la consulta)\n"))

# Hay dos opciones de extracción de los datos:

opcion = input("Elige opción: \n 1) Descargar los csv \n 2) Extraer los datos del html \n")

# Usamos la función buscalinks para rastrear todos los
# links internos

a = buscalinks(url, "a", "class", "enlace_3er_nvl")

# Se selecciona el link que interesa: "ultimos datos" y se crea
# una nueva dirección url. Para ello se llama la función linkunico
# que busca el único link válido. En caso de que encuentre más
# de uno, devuelve error.

sub = "ultimosdatos"

link = linkunico(a, sub)

url2 = url + link

# En el nuevo link generado, hay que seleccionar las opciones
# Resumen días anteriores y tablas. 

link = buscalinks (url2, "a", "title", "Resúmenes diarios anteriores")

url3 = url + link

# Se selecciona la opción tablas:

link = buscalinks (url3, "a", "text", "Tabla")

url4 = url + link

# Ahora se tiene el url de la web en la que se va a trabajar.

if opcion == "1":

#Opción 1: descargar los csv:

# Primero se obtiene la url de los csv:

    link = buscalinks (url4, "div", "class", "enlace_csv inline_block", dep = 2, tag2 = "a")

    links = linksgen(d, link, url)

# Después se cargan todos los csv, añadiendo a cada uno una columna con su fecha:

    df = cargacsv(links)
    
if opcion == "2":

    # En vez de buscar los links de los csv, se busca los links de las webs que cargan
    # en el html de la página los datos requeridos. Primero se obtiene el link del
    # primer enlace y a partir de ese, se sacan los links de los demás días:

    link = buscalinks (url4, "div", "class", "boton activo", dep = 2, tag2 = "a")

    # Salen las dos veces que aparece el link, nos quedamos solo con uno de los links

    link = link[0]
    
    #Se generan todos los links

    links = linksgen(d, link, url)

    #Se rellena un dataframe con la información de cada página web

    df = dathtml (links)

#Una vez creado el dataFrame, se hace un pequeña manipulación en los datos.
# Algunas columnas ( Tmax, Tmin, Racha y Vmax además de tener los datos de temperatura, tienen
# las horas. Esta información se va a separar.

campos = list( list(df)[i] for i in [2,3,5,6])

df = limphora(df, campos)

# Finalmente, se descarga el DataFrame en el equipo con formato csv.

tiempo = time.strftime("%d-%m-%y")

archivo = "municipiosespaña_descarga_" + tiempo + ".csv"

df.to_csv(archivo, encoding='latin-1', index=False)

print( "Descarga en el equipo completada")


