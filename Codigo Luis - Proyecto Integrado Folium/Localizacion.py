import sys
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
from test import *

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine


warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)

class Localizar():


	def area_especifica(area):

		sugerencias = []
		contador = 0
		#print(myjson) Imprimir contenido del json, features, properties, coordinates
		while (len(sugerencias)==0):

			if(len(sugerencias)==0 and contador>0):
				area = input("\n\tIntroducir un area_especifica --> ")

			myjson = search_api(area)
			for i in range(len(myjson["features"])):
				if(myjson["features"][i]["properties"]["country"]=="Peru"):
					address_line1 = myjson["features"][i]["properties"]["address_line1"]
					formatted = myjson["features"][i]["properties"]["formatted"]
					print(f"\nSugerencia N°{i+1}: --> {formatted}")
					sugerencias.append(address_line1)

			contador = contador + 1

		seleccionFinal = int(input("\n\tSeleccionar N° de Sugerencia -> : "))

		while(seleccionFinal>len(sugerencias) or seleccionFinal<0):
			print("\n\tSeleccione un valor correcto..")
			seleccionFinal = int(input("\n\tSeleccionar N° de Sugerencia -> : "))

		latitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][1]
		longitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][0]
		coordenadas = [latitud,longitud]
		

		print(f"\n\tHas seleccionado la sugerencia {seleccionFinal} para el area especifica.\n")

		return area,coordenadas

	def busqueda_sugerencias(lugar):
		sugerencias = []

		#print(myjson) Imprimir contenido del json, features, properties, coordinates
		contador = 0
		while (len(sugerencias)==0):

			if(len(sugerencias)==0 and contador>0):
				lugar = input("\n\tIntroducir un area_especifica --> ")

			myjson = search_api(lugar)

			for i in range(len(myjson["features"])):
				if(myjson["features"][i]["properties"]["country"]=="Peru"):
					address_line1 = myjson["features"][i]["properties"]["address_line1"]
					formatted = myjson["features"][i]["properties"]["formatted"]
					print(f"\nSugerencia N°{i+1}: --> {formatted}")
					sugerencias.append(address_line1)

			contador = contador + 1

		seleccionFinal = int(input("\n\tSeleccionar N° de Sugerencia -> : "))

		while(seleccionFinal>len(sugerencias) or seleccionFinal<0):
			print("\nSeleccione un valor correcto..")
			seleccionFinal = int(input("\nSeleccionar N° de Sugerencia -> : "))

		latitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][1]
		longitud = myjson["features"][seleccionFinal-1]["geometry"]["coordinates"][0]
		coordenadas = [latitud,longitud]
		

		print(f"\n\tHas seleccionado la sugerencia {seleccionFinal} para el nodo.\n")

		return sugerencias[seleccionFinal-1],coordenadas

class drawFolium():
	def save_map(coordenadas_area,coordenadas_inicio,coordenadas_destino,area_especifica):
		G = ox.graph_from_point(coordenadas_area, dist=5000, simplify=True, network_type="walk")
		origin_point = (coordenadas_inicio[0],coordenadas_inicio[1]) 
		destination_point = (coordenadas_destino[0],coordenadas_destino[1]) 

		origin_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0]) #nearest_nodes recibe en orden longitud,latitud
		print('origin_node',origin_node)
		destination_node = ox.distance.nearest_nodes(G, destination_point[1], destination_point[0])
		print('destination_node',destination_node)
		routeFolium = ox.distance.shortest_path(G, origin_node,destination_node)

		#Stamen Terrain
		mapatest = ox.plot_route_folium(G, routeFolium, popup_attribute='length',tiles="OpenStreetMap", color='red')
		mapatest.save(f"{area_especifica}.html")
		global area_esp
		area_esp = area_especifica
		

	def show_pyqt():
		display_pyqt.main(area_esp)
		os.system("cls")
	

def search_api(lugar):

	url = (f"https://api.geoapify.com/v1/geocode/autocomplete?text={lugar}&apiKey=2e9ba25ff3ca47d0b02d81540edbafdd")
	headers = CaseInsensitiveDict()
	headers["Accept"] = "application/json"
	resp = requests.get(url, headers=headers)
	myjson = resp.json()

	return myjson