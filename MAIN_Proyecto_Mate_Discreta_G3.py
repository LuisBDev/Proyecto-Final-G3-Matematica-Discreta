import os
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pyproj import CRS
import contextily as ctx
import warnings
from shapely.geometry import LineString, Point
import folium
from Localizacion import *
from DijkstraMain import *
from floyd_warshall_mdv2 import *



warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)


def obtener_area_especifica():

    print("\n##### [BÚSQUEDA ÁREA ESPECÍFICA.] #####")
    area = input("\n\tIntroducir area_especifica --> ")
    global area_especifica
    global coordenadas_area
    area_especifica, coordenadas_area = Localizar.area_especifica(area)

    print(f"Coordenadas area_especifica: {coordenadas_area[0],coordenadas_area[1]}")

def menu_implementacion():
    os.system("cls")
    opcion = int(input("\n\n\t1. Mostrar matplotlib.\n\t2. Mostrar background\n\t3. Mostrar folium.\n\t0. Salir\n\n\t--> "))
    if(opcion==0):
        sys.exit()
    while(opcion!=0):
        if(opcion == 1):
            plot_matplotlib()
        elif(opcion==2):
            plot_background()
        elif(opcion == 3):
            drawFolium.show_pyqt()

        opcion = int(input("\n\n\t1. Mostrar matplotlib.\n\t2. Mostrar background\n\t3. Mostrar folium.\n\t0. Salir\n\n\t--> "))
        if(opcion==0):
            sys.exit()

def proyectar_grafo():
    global graph
    graph = ox.graph_from_place(area_especifica, network_type='drive')

    # Obtener el polígono del área de interés
    place_polygon = ox.geocode_to_gdf(area_especifica)

    # Volver a proyectar el polígono a un CRS local proyectado
    place_polygon = place_polygon.to_crs(epsg=3067)

    # Buffer
    place_polygon["geometry"] = place_polygon.buffer(200)

    # Volver a proyectar el polígono a WGS84, según requerimiento de osmnx
    place_polygon = place_polygon.to_crs(epsg=4326)

    # recuperar el grafo
    graph = ox.graph_from_polygon(place_polygon["geometry"].values[0], network_type='drive')

    # Recuperar solo los bordes o aristas del gráfico
    global edges
    edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # Proyectar el grafo
    global graph_proj
    graph_proj = ox.project_graph(graph)

    # Obtener bordes y nodos
    global nodes_proj, edges_proj
    nodes_proj, edges_proj = ox.graph_to_gdfs(
        graph_proj, nodes=True, edges=True)


def input_origen():
    # Pedir al usuario que ingrese el nodo de inicio.

    # Mostramos las sugerencias de búsqueda y guardamos tanto como las coordenadas y el nombre del nodo de inicio.
    global nodo_inicio, coordenadas_inicio
    inicio = input("\n##### [BÚSQUEDA DEL NODO DE ORIGEN.] #####\n\t --> ")
    nodo_inicio, coordenadas_inicio = Localizar.busqueda_sugerencias(inicio)

    print(coordenadas_inicio)  # Imprimir coordenadas del nodo de inicio

    # Geocodificar el nombre del lugar
    geocoded_place = ox.geocode_to_gdf(nodo_inicio, which_result=1)

    # Re-proyectar en el mismo CRS que la red vial
    geocoded_place = geocoded_place.to_crs(CRS(edges_proj.crs))

    # Obtener centroide como punto shapely
    global origin
    origin = geocoded_place["geometry"].centroid.values[0]


def input_destino():
    # Pedir al usuario que ingrese el nodo de destino.

    # Mostramos las sugerencias de búsqueda y guardamos tanto como las coordenadas y el nombre del nodo de destino.
    global nodo_destino, coordenadas_destino
    destino = input("\n##### [BÚSQUEDA DEL NODO DE DESTINO.] #####\n\t --> ")
    nodo_destino, coordenadas_destino = Localizar.busqueda_sugerencias(destino)

    print(coordenadas_destino)  # Imprimir coordenadas del nodo de destino

    # Geocodificar el nodo_destino
    geocoded_place = ox.geocode_to_gdf(nodo_destino, which_result=1)

    # Recuperar solo los bordes o aristas del gráfico
    geocoded_place = geocoded_place.to_crs(CRS(edges_proj.crs))

    # Obtener centroide como punto shapely
    global destination
    destination = geocoded_place["geometry"].centroid.values[0]


def ubicar_nearest_nodes():
    # Hallaremos el nodo en el gráfico que está más cerca del punto de origen
    # (aquí, queremos obtener el ID del nodo)
    global orig_node_id
    orig_node_id = ox.nearest_nodes(graph_proj, origin.x, origin.y)
    print(f"\n------> ID Nodo Origen: {orig_node_id}")

    # Hallaremos el nodo en el gráfico que está más cerca del punto de destino
    # (aquí, queremos obtener el ID del nodo)
    global target_node_id
    target_node_id = ox.nearest_nodes(graph_proj, destination.x, destination.y)
    print(f"\n------> ID Nodo Destino: {target_node_id}")

################################################################################################

# Recupere las filas de los nodos GeoDataFrame según la identificación del nodo
# (la identificación del nodo es la etiqueta de índice)


def filtrar_nodos():
    orig_node = nodes_proj.loc[orig_node_id]
    target_node = nodes_proj.loc[target_node_id]

    # Crear un GeoDataFrame a partir de los puntos de origen y destino
    global od_nodes
    od_nodes = gpd.GeoDataFrame(
        [orig_node, target_node], geometry='geometry', crs=nodes_proj.crs)


def check_path():
	# Verificar si existe un path y luego calcular el shortest path
	try:
		global route
		route = nx.shortest_path(G=graph_proj, source=orig_node_id, target=target_node_id, weight='length')
	except nx.NetworkXNoPath:
		print(f"No se ha podido calcular el camino mínimo por el momento.\nIntente con otros nodos.")
		return False
	else:
		return True

# Plottear el shortest path con matplotlib
#fig, ax = ox.plot_graph_route(graph_proj, route)

def crear_dataframe_route():
    # Obtener los nodos a lo largo del camino más corto (shortest path)
    route_nodes = nodes_proj.loc[route]

    # Crear una geometría para la ruta más corta
    route_line = LineString(list(route_nodes.geometry.values))

    # Crear un GeoDataFrame
    global route_geom
    route_geom = gpd.GeoDataFrame(
        [[route_line]], geometry='geometry', crs=edges_proj.crs, columns=['geometry'])


def plottear_elementos():
    # Aqui se puede agregar mas tags.
    tags = {'building': True}

    buildings = ox.geometries_from_place(area_especifica, tags)

    buildings_proj = buildings.to_crs(CRS(edges_proj.crs))

    global ax
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plottear nodos y aristas

    edges_proj.plot(ax=ax, linewidth=0.75, color='gray')
    nodes_proj.plot(ax=ax, markersize=2, color='gray')

    # Plottear edificios - buildings
    ax = buildings_proj.plot(ax=ax, facecolor='lightgray', alpha=0.7)

    # Plottear la ruta
    ax = route_geom.plot(ax=ax, linewidth=2, linestyle='--', color='red')

    # Agregar los nodos de origen y destino de la ruta
    ax = od_nodes.plot(ax=ax, markersize=30, color='blue')

    # Agregar mapa base usando contextily
    ctx.add_basemap(ax, crs=buildings_proj.crs,source=ctx.providers.OpenStreetMap.Mapnik)


def plot_matplotlib():
    ax.set_axis_off()
    plt.title("Optimización de Trayectos")
    plt.show()
    #menu_implementacion()

def plot_background():
    global bbox
    bbox = ox.utils_geo.bbox_from_point(point=(coordenadas_inicio[0], coordenadas_inicio[1]), dist=5000)
    bgcolor = "#061529"
    fig, ax = ox.plot_graph_route(graph, route, bbox = bbox, route_linewidth=6, node_size=0, bgcolor=bgcolor,dpi = 300)
    
def medio_de_transporte():
    medio = int(input("\nEn qué medio desea transportarse\n\t1. Caminando.\n\t2. Auto.\n\t3. Bicicleta.\n\t0. Salir\n\n\t--> "))
    while (medio != 0):
        os.system("cls")
        if(medio == 1):
            return "walk"

        elif(medio == 2):
            return "drive"

        elif(medio == 3):
            return "bike"

def save_folium():
    #ox.config(use_cache=True)
    medio=medio_de_transporte()
    drawFolium.save_map(coordenadas_area, coordenadas_inicio,coordenadas_destino, area_especifica,medio)
    os.system("cls")


def implementacion_vial():
    obtener_area_especifica()
    proyectar_grafo()
    input_origen()
    input_destino()
    ubicar_nearest_nodes()
    filtrar_nodos()
    check_path()
    crear_dataframe_route()
    plottear_elementos()

    # Folium

    save_folium()

    # Matplotlib


def menu_algoritmos():
    opcion = int(input("\nSeleccionar el grafo a implementar:\n\n\t1. Floyd Warshall\n\t2. Dijkstra\n\t3. Implementacion Vial\n\t0. Salir de la aplicacion.\n\n\t\t---> "))
    while (opcion != 0):

        if(opcion == 1):
            display_floyd_warshall.main()
            os.system("cls")

        elif(opcion == 2):
            display_dijkstra.main()
            os.system("cls")

        elif(opcion == 3):
            implementacion_vial()
            os.system("cls")
            menu_implementacion()

        opcion = int(input("\nSeleccionar el grafo a implementar:\n\n\t1. Floyd Warshall\n\t2. Dijkstra\n\t3. Implementacion\n\t0. Salir de la aplicacion.\n\n\t\t---> "))


menu_algoritmos()
