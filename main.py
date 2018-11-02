from functions import buscalinks

from functions import linkunico

from functions import linksgen

from functions import cargacsv

from functions import limphora

from functions import dathtml

import urllib.request

import time

import os

import sys

# Definimos la url principal

url = "http://www.aemet.es"

# Guardamos la ubicación del código para guardar los archivos:

ruta = os.path.dirname(sys.argv[0])

#Se pide introducir el número de días que se quiere descargar.

d = int(input("¿De cuantos días deseas descargar información?\n(AEMET permite hasta los 7 días anteriores a la consulta)\n"))

# Aseguramos que la respuesta introducida es válida

while (d < 1 or d > 7):
    print ("Tu respuesta debe ser un entero entre 1 y 7")
    d = int(input("¿De cuantos días deseas descargar información?\n(AEMET permite hasta los 7 días anteriores a la consulta)\n"))


# Hay dos opciones de extracción de los datos:

opcion = int(input("Elige opción: \n 1) Descargar los csv \n 2) Extraer los datos del html \n"))

# Aseguramos que la respuesta introducida es válida

while (opcion < 1 or opcion > 2):
    print ("Tu respuesta debe ser 1 (Opción 1) o 2 (Opción 2)")
    opcion = int(input("Elige opción: \n 1) Descargar los csv \n 2) Extraer los datos del html \n"))


#Se pregunta al usuario si quiere tambien descargar el mapa de la temperatura del mar

mapa = input ("¿Quieres también descargar el mapa de la temperatura del mar? \n (Escribe S o N)\n").upper()

# Aseguramos que la respuesta introducida es válida

while (mapa != "S" and mapa != "N"):
    print ("Tu respuesta debe S o N")
    mapa = input ("¿Quieres también descargar el mapa de la temperatura del mar? \n (Escribe S o N)\n").upper()
    
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

if opcion == 1:

#Opción 1: descargar los csv:

# Primero se obtiene la url de los csv:

    link = buscalinks (url4, "div", "class", "enlace_csv inline_block", dep = 2, tag2 = "a")

    links = linksgen(d, link, url)

# Después se cargan todos los csv, añadiendo a cada uno una columna con su fecha:

    df = cargacsv(links)
    
if opcion == 2:

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

# Una vez creado el dataFrame, se hace un pequeña manipulación en los datos.
# Algunas columnas ( Tmax, Tmin, Racha y Vmax además de tener los datos de temperatura, tienen
# las horas. Esta información se va a separar.

campos = list( list(df)[i] for i in [2,3,5,6])

df = limphora(df, campos)

# Finalmente, se descarga el DataFrame en el equipo con formato csv.

tiempo = time.strftime("%d-%m-%y")

archivo = "\csv\municipiosespaña_descarga_" + tiempo + ".csv"

df.to_csv(ruta + archivo, encoding='latin-1', index=False)

print( "Descarga del csv en el equipo completada")

# Ahora toca, en caso de que se haya seleccionado, descargar la imagen requerida:

if mapa == 'S':

    # Llamamos a la función linkunico, pero ahora vamos a buscar por satélite, que nos llevará a la sección que guarda el mapa:

    sub = "satelite"

    link = linkunico(a, sub)

    urls = url + link

    # Ahora se selecciona el link que lleva a Productos derivados

    link = buscalinks (urls, "a", "title", "Productos derivados")

    urlpd = url + link

    # Y finalmente al link que lleva al mapa de la temperatura del agua del mar:

    link = buscalinks (urlpd, "a", "text", "Temperatura del agua del mar")

    urlm = url + link
    
    # Se obtiene el link a la imagen

    link = buscalinks (urlm, "img", "class", "pdtop10", ref = "src")

    urlimg = url + link

    # Y se guarda en la carpeta "imagenes"

    urllib.request.urlretrieve(urlimg, ruta + '\\imagenes\\' + tiempo + "_mapa_temp_mar.gif")

    print ("Descarga del mapa de temperatura del agua del mar en el equipo completada")


