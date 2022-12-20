# Proyecto-Final-G3-Matematica-Discreta

Requerimientos instalación vía pip en el archivo de texto requirements.txt

Instalación: pip install -r requirements.txt

FUNCIONAMIENTO:

Ejecutar MAIN_Proyecto_Mate_Discreta_G3 y se mostrará el siguiente menú:

#--------------------------------------------------------------------------------------#

Seleccionar el grafo a implementar:

        1. Floyd Warshall
        2. Dijkstra
        3. Implementacion Vial
        0. Salir de la aplicacion.

                ---> 3

#--------------------------------------------------------------------------------------#

Seleccionamos la primera opción para desplegar el funcionamiento de Floyd Warshall.

Seleccionamos la segunda opción para desplegar el funcionamiento de Dijkstra.

Seleccionamos la tercera opción para desplegar el funcionamiento de la Implementación Vial.

CASO DE USO: (Selección de opción 3 [Implementación Vial])
Al acceder a la opción 3, nos pedirá un área específica en la cual se trabajará para graficar el mapa.

#--------------------------------------------------------------------------------------#

##### [BÚSQUEDA ÁREA ESPECÍFICA.]

        Introducir area_especifica --> La Molina, Lima, Peru

#--------------------------------------------------------------------------------------#

En el archivo de texto se encuentran algunas pruebas unitarias que podemos usar (son casos validados).
Por ejemplo, en area_especifica, podemos introducir: La Molina, Lima, Peru

## Se mostrarán algunas sugerencias relacionadas a tu búsqueda:

#--------------------------------------------------------------------------------------#

Sugerencia N°1: --> La Molina, LIM, Peru

Sugerencia N°2: --> Lima, La Molina 15012, Peru

Sugerencia N°3: --> La Molina, Jirón El Haras, La Molina 15051, Peru

Sugerencia N°4: --> Javier Prado, La Molina Avenue, La Molina 012, Peru

        Seleccionar N° de Sugerencia -> : 1

#--------------------------------------------------------------------------------------#

Seleccionamos, por ejemplo, la sugerencia de búsqueda N° 1. (Escribimos 1).

## Se mostrará las coordenadas del area_especifica que elegiste:

#--------------------------------------------------------------------------------------#

Has seleccionado la sugerencia 1 para el area especifica.

Coordenadas area_especifica: (-12.0901768, -76.92233779667893)

#--------------------------------------------------------------------------------------#

##### [BÚSQUEDA DEL NODO DE ORIGEN.]

         --> Ovalo La Fontana, La Molina, Peru

En este apartado ponemos el punto de inicio para hallar la ruta mas corta.
(Ejemplo: Ovalo La Fontana, La Molina, Peru)

#--------------------------------------------------------------------------------------#

Sugerencia N°1: --> Óvalo La Fontana, La Molina 012, Peru

        Seleccionar N° de Sugerencia -> : 1

#--------------------------------------------------------------------------------------#

(Seleccionamos la sugerencia N° 1.)

## Se mostrará las coordenadas del nodo de origen que elegiste:

Has seleccionado la sugerencia 1 para el nodo.

[-12.07388755, -76.95553541251871]

#--------------------------------------------------------------------------------------#

##### [BÚSQUEDA DEL NODO DE DESTINO.]

         --> Molicentro, La Molina, Lima, Peru

En este apartado ponemos el punto de destino para hallar la ruta mas corta.

(Ejemplo: Molicentro, La Molina, Lima, Peru)

#--------------------------------------------------------------------------------------#

## Se mostrarán algunas sugerencias relacionadas a tu búsqueda:

Sugerencia N°1: --> Molicentro, La Molina, La Molina 15051, Peru

Sugerencia N°2: --> Molicentro, Avenida La Molina, La Molina, La Molina 15026, Peru

Sugerencia N°3: --> MoliCentro, La Molina Avenue, La Molina, La Molina 15051, Peru

Sugerencia N°4: --> Molicentro, La Molina Avenue, La Molina, La Molina 15026, Peru

        Seleccionar N° de Sugerencia -> : 2

(Escribimos el número de sugerencia de búsqueda 2 por ejemplo).

#--------------------------------------------------------------------------------------#

## Se mostrará las coordenadas del nodo de destino que elegiste y sus ID's:

[-12.0816175, -76.9285181]

------> ID Nodo Origen: 9490435743

------> ID Nodo Destino: 3789484199

## Seleccionamos el medio de transporte para realizar la ruta.

En qué medio desea transportarse

1.  Caminando.

2.  Auto.

3.  Bicicleta.

4.  Salir

        --> 2

(Ejemplo, escribimos número 2 para indicar que el trayecto será vía auto).

## Seleccionamos la opción que queremos visualizar (En este orden -> 1,2,3).

## Seleccionamos matplotlib digitando la opción 1

        1. Mostrar matplotlib.
        2. Mostrar background
        3. Mostrar folium.
        0. Salir

        --> 1

Luego de haber visualizado matplotlib podemos CERRARLO e ir a la segunda opción.

## Seleccionamos la opción que queremos visualizar.

## Seleccionamos background digitando la opción 2

        1. Mostrar matplotlib.
        2. Mostrar background
        3. Mostrar folium.
        0. Salir

        --> 2

Luego de haber visualizado background podemos CERRARLO e ir a la tercera opción y la más importante.

## Seleccionamos la opción que queremos visualizar.

## Mostramos el mapa interactivo a través de folium digitando la opción 3

        1. Mostrar matplotlib.
        2. Mostrar background
        3. Mostrar folium.
        0. Salir

        --> 3

### Finalización del programa.
