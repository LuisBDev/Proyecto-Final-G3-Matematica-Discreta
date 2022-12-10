import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pyproj import CRS
import contextily as ctx
import warnings
from locat import Localizar
from shapely.geometry import LineString, Point

warnings.filterwarnings("ignore", category=DeprecationWarning) 

area_limit = "Lima,Peru"

# Retrieve the network
grafica = ox.graph_from_place(area_limit, network_type='drive')

# Get the area of interest polygon
area_poligonal = ox.geocode_to_gdf(area_limit)

# Re-project the polygon to a local projected CRS 
area_poligonal = area_poligonal.to_crs(epsg=3067)

# Buffer a bit
area_poligonal["geometry"] = area_poligonal.buffer(200)

# Re-project the polygon back to WGS84, as required by osmnx
area_poligonal = area_poligonal.to_crs(epsg=4326)

# Retrieve the network
grafica = ox.graph_from_polygon(area_poligonal["geometry"].values[0], network_type='bike')

# Retrieve only edges from the graph
bordes = ox.graph_to_gdfs(grafica, nodes=False, edges=True)

# Project the data
graph_proj = ox.project_graph(grafica)

# Get Edges and Nodes
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)

# Set place name
punto_inicio = Localizar.busqueda_inicio()

# Geocode the place name...poner coordenada en el mapa
area_geocode = ox.geocode_to_gdf(punto_inicio, which_result=1)

# Re-project into the same CRS as the road network
area_geocode = area_geocode.to_crs(CRS(edges_proj.crs))

# Get centroid as shapely point
origen = area_geocode["geometry"].centroid.values[0]

# Set place name2
punto_final = Localizar.busqueda_destino()

# Geocode the place name
area_geocode = ox.geocode_to_gdf(punto_final, which_result=1)

# Re-project into the same CRS as the road network
area_geocode = area_geocode.to_crs(CRS(edges_proj.crs))

# Get centroid of the polygon as shapely point
destino = area_geocode["geometry"].centroid.values[0]

# Find the node in the graph that is closest to the origin point (here, we want to get the node id)
orig_node_id = ox.nearest_nodes(graph_proj, origen.x,origen.y)

# Find the node in the graph that is closest to the target point (here, we want to get the node id)
target_node_id = ox.nearest_nodes(graph_proj, destino.x,destino.y)
#Hasta aquí
################################################################################################

# Retrieve the rows from the nodes GeoDataFrame based on the node id (node id is the index label)
nodo_origen = nodes_proj.loc[orig_node_id]
objetivo_nodo = nodes_proj.loc[target_node_id]

# Create a GeoDataFrame from the origin and target points
od_nodes = gpd.GeoDataFrame([nodo_origen, objetivo_nodo], geometry='geometry', crs=nodes_proj.crs)

# Calculate the shortest path
ruta = nx.shortest_path(G=graph_proj, source=orig_node_id, target=target_node_id, weight='length')

# Get the nodes along the shortest path
nodo_ruta = nodes_proj.loc[ruta]

# Create a geometry for the shortest path
linea_ruta = LineString(list(nodo_ruta.geometry.values))

# Create a GeoDataFrame
geom_ruta = gpd.GeoDataFrame([[linea_ruta]], geometry='geometry', crs=edges_proj.crs, columns=['geometry'])

#################################################################################

#Aqui se puede agregar mas tags.
tags = {'building': True}

constu = ox.geometries_from_place(area_limit, tags)

proyecto_constru = constu.to_crs(CRS(edges_proj.crs))

fig, ax = plt.subplots(figsize=(12,8))

# Plot edges and nodes

edges_proj.plot(ax=ax, linewidth=0.75, color='gray')
nodes_proj.plot(ax=ax, markersize=2, color='gray')


# Add buildings
ax = proyecto_constru.plot(ax=ax, facecolor='lightgray', alpha=0.7)

# Add the route
ax = geom_ruta.plot(ax=ax, linewidth=2, linestyle='--', color='red')

# Add the origin and destination nodes of the route
ax = od_nodes.plot(ax=ax, markersize=30, color='red')

# Add basemap
ctx.add_basemap(ax, crs=proyecto_constru.crs, source=ctx.providers.OpenStreetMap.Mapnik)
ax.set_axis_off()
plt.title("Optimización de Trayectos")
plt.show()




