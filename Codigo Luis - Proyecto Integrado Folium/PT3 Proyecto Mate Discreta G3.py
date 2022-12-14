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
from Localizacion import *
import folium


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)


area_especifica = input("Introducir area_especifica: ")
coordenadas_area = Localizar.area_especifica(area_especifica)
print(f"Coordenadas area_especifica: {coordenadas_area[0],coordenadas_area[1]}")

# recuperar el grafo
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
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

# Proyectar el grafo
graph_proj = ox.project_graph(graph)

# Obtener bordes y nodos
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges =True)

#Pedir al usuario que ingrese el nodo de inicio.
inicio = input("Introducir el nodo de inicio: ")

#Mostramos las sugerencias de búsqueda y guardamos tanto como las coordenadas y el nombre del nodo de inicio.
nodo_inicio,coordenadas_inicio = Localizar.busqueda_sugerencias(inicio)

print(coordenadas_inicio) #Imprimir coordenadas del nodo de inicio

# Geocodificar el nombre del lugar
geocoded_place = ox.geocode_to_gdf(nodo_inicio,which_result=1)

# Re-proyectar en el mismo CRS que la red vial
geocoded_place = geocoded_place.to_crs(CRS(edges_proj.crs))

# Obtener centroide como punto shapely
origin = geocoded_place["geometry"].centroid.values[0]


#Pedir al usuario que ingrese el nodo de destino.
destino = input("Introducir el nodo de destino: ")

#Mostramos las sugerencias de búsqueda y guardamos tanto como las coordenadas y el nombre del nodo de destino.
nodo_destino,coordenadas_destino = Localizar.busqueda_sugerencias(destino)
print(coordenadas_destino) #Imprimir coordenadas del nodo de destino



# Geocodificar el nodo_destino
geocoded_place = ox.geocode_to_gdf(nodo_destino,which_result=1)

# Recuperar solo los bordes o aristas del gráfico
geocoded_place = geocoded_place.to_crs(CRS(edges_proj.crs))

# Obtener centroide como punto shapely
destination = geocoded_place["geometry"].centroid.values[0]

# Hallaremos el nodo en el gráfico que está más cerca del punto de origen 
# (aquí, queremos obtener el ID del nodo)
orig_node_id = ox.nearest_nodes(graph_proj, origin.x,origin.y)

# Hallaremos el nodo en el gráfico que está más cerca del punto de destino 
# (aquí, queremos obtener el ID del nodo)
target_node_id = ox.nearest_nodes(graph_proj, destination.x,destination.y)

################################################################################################

# Recupere las filas de los nodos GeoDataFrame según la identificación del nodo 
# (la identificación del nodo es la etiqueta de índice)

orig_node = nodes_proj.loc[orig_node_id]
target_node = nodes_proj.loc[target_node_id]

# Crear un GeoDataFrame a partir de los puntos de origen y destino
od_nodes = gpd.GeoDataFrame([orig_node, target_node], geometry='geometry', crs=nodes_proj.crs)



def check_path():
	# Verificar si existe un path y luego calcular el shortest path
	try:
		route = nx.shortest_path(G=graph_proj, source=orig_node_id, target=target_node_id, weight='length')

	except nx.NetworkXNoPath:
	    print(f"No se ha podido calcular el camino mínimo por el momento.\nIntente con otros nodos.")
	    return False

	return route


route = check_path()


# Plottear el shortest path con matplotlib
#fig, ax = ox.plot_graph_route(graph_proj, route)

# Obtener los nodos a lo largo del camino más corto (shortest path)
route_nodes = nodes_proj.loc[route]

# Crear una geometría para la ruta más corta
route_line = LineString(list(route_nodes.geometry.values))


# Crear un GeoDataFrame
route_geom = gpd.GeoDataFrame([[route_line]], geometry='geometry', crs=edges_proj.crs, columns=['geometry'])


#Aqui se puede agregar mas tags.
tags = {'building': True}

buildings = ox.geometries_from_place(area_especifica, tags)

buildings_proj = buildings.to_crs(CRS(edges_proj.crs))

fig, ax = plt.subplots(figsize=(12,8))

# Plot edges and nodes

edges_proj.plot(ax=ax, linewidth=0.75, color='gray')
nodes_proj.plot(ax=ax, markersize=2, color='gray')


# Plottear edificios - buildings
ax = buildings_proj.plot(ax=ax, facecolor='lightgray', alpha=0.7)

# Plottear la ruta
ax = route_geom.plot(ax=ax, linewidth=2, linestyle='--', color='red')

# Agregar los nodos de origen y destino de la ruta
ax = od_nodes.plot(ax=ax, markersize=30, color='red')

# Agregar mapa base usando contextily
ctx.add_basemap(ax, crs=buildings_proj.crs, source=ctx.providers.OpenStreetMap.Mapnik)


#ax.set_axis_off()
#plt.title("Optimización de Trayectos")
#plt.show()

############################################# Folium

ox.config(log_console=True, use_cache=True)
drawFolium.save_map(coordenadas_area,coordenadas_inicio,coordenadas_destino,area_especifica)

ax.set_axis_off()
plt.title("Optimización de Trayectos")
plt.show()

