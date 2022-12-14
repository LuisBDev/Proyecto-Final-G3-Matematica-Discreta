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

import requests
from requests.structures import CaseInsensitiveDict

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

class Localizar():


	def area_especifica(area):
		sugerencias = []
		url = (f"https://api.geoapify.com/v1/geocode/autocomplete?text={area}&apiKey=2e9ba25ff3ca47d0b02d81540edbafdd")
		headers = CaseInsensitiveDict()
		headers["Accept"] = "application/json"
		resp = requests.get(url, headers=headers)
		myjson = resp.json()

		print(myjson)

		for i in range(len(myjson["features"])):
			if(myjson["features"][i]["properties"]["country"]=="Peru"):
				address_line1 = myjson["features"][i]["properties"]["address_line1"]
				formatted = myjson["features"][i]["properties"]["formatted"]
				print(f"\nSugerencia N°{i+1}: --> {formatted}")
				sugerencias.append(address_line1)


		seleccionFinal = int(input("\nSeleccionar N° de Sugerencia -> : "))

		while(seleccionFinal>len(sugerencias) or seleccionFinal<0):
			print("\nSeleccione un valor correcto..")
			seleccionFinal = int(input("\nSeleccionar N° de Sugerencia -> : "))

		latitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][1]
		longitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][0]
		coordenadas = [latitud,longitud]
		

		print(f"\nHas seleccionado la sugerencia {seleccionFinal} para el area especifica.\n")

		return coordenadas

	def busqueda_sugerencias(lugar):
		sugerencias = []
		url = (f"https://api.geoapify.com/v1/geocode/autocomplete?text={lugar}&apiKey=2e9ba25ff3ca47d0b02d81540edbafdd")
		headers = CaseInsensitiveDict()
		headers["Accept"] = "application/json"
		resp = requests.get(url, headers=headers)
		myjson = resp.json()

		print(myjson)

		for i in range(len(myjson["features"])):
			if(myjson["features"][i]["properties"]["country"]=="Peru"):
				address_line1 = myjson["features"][i]["properties"]["address_line1"]
				formatted = myjson["features"][i]["properties"]["formatted"]
				print(f"\nSugerencia N°{i+1}: --> {formatted}")
				sugerencias.append(address_line1)


		seleccionFinal = int(input("\nSeleccionar N° de Sugerencia -> : "))

		while(seleccionFinal>len(sugerencias) or seleccionFinal<0):
			print("\nSeleccione un valor correcto..")
			seleccionFinal = int(input("\nSeleccionar N° de Sugerencia -> : "))

		latitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][1]
		longitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][0]
		coordenadas = [latitud,longitud]
		

		print(f"\nHas seleccionado la sugerencia {seleccionFinal} para el nodo.\n")

		return sugerencias[seleccionFinal-1],coordenadas

class drawFolium():
	def save_map(coordenadas_area,coordenadas_inicio,coordenadas_destino):
		G = ox.graph_from_point(coordenadas_area, dist=5000, simplify=True, network_type="drive")
		origin_point = (coordenadas_inicio[0],coordenadas_inicio[1]) 
		destination_point = (coordenadas_destino[0],coordenadas_destino[1]) 

		origin_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0]) #nearest_nodes recibe en orden longitud,latitud
		print('origin_node',origin_node)
		destination_node = ox.distance.nearest_nodes(G, destination_point[1], destination_point[0])
		print('destination_node',destination_node)
		routeFolium = ox.distance.shortest_path(G, origin_node,destination_node)


		mapatest = ox.plot_route_folium(G, routeFolium, popup_attribute='length',tiles="OpenStreetMap", color='red')
		mapatest.save("testmapa.html")
