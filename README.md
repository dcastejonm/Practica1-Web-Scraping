# Practica1-Web-Scraping

## Breve descripción

Primera práctica de la asignatura _Tipología y ciclo de vida de los datos_ del Master Ciencia de Datos de la _Universidad Oberta de Catalunya_. Se aplican técnicas de _web scraping_ para extraer la información meteorológica de todos los municipios de España de la página web de la Agencia Nacional de Meteorología (AEMET). En particular, se extrae la información de la pestaña últimos datos, permitiendo al usuario seleccionar el número de días de los que quiere descargar la información. (AEMET permite la descarga de los datos de hasta los 7 días previos al día de consulta). Además, también permite descargar el mapa de la temperatura del agua del mar, en caso de que el usuario así lo quiera.

## Archivos del código y ejecución

- **main.py**: Corre el código principal. Es el archivo a correr para realizar la descarga de los datos.
- **functions.py**: Define todas las funciones que se usan en el archivo main.py.

Para ejecutar, se corre el archivo main.py. Posteriormente, en la consola se preguntará al usuario cuantos días quiere descargar y qué método prefiere usar para realizar la descarga de los datos:

1. La opción 1 busca el botón de los csv en la web de AEMET y descarga la información desde dicho link. Luego agrupa todos los datos en un único archivo y realiza una limpieza preliminar de los datos.
2. La opción 2 busca en el html de la página web toda la información necesaria. Agrupa toda la infomación en un único archivo y realiza una limpieza preliminar de los datos.

Finalmente, preguntará al usuario si desea descargar el mapa de temperatura del agua del mar

Para consultar sobre la licencia y la estructura de los datos, accede a la carpeta informacion y lee el documento que contiene.

## Librerías necesarias

- **urllib**
- **bs4**
- **pandas**
- **numpy**

## Miembros del equipo

La actividad ha sido realizada por Diego Castejón Molina

## Bibliografía

- Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
- Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC
