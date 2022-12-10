import json
import requests
from requests.structures import CaseInsensitiveDict

class Localizar():

    def busqueda_inicio():
        lugar=input("Intoducir lugar de inicio: ")
        resp=api_search(lugar)
        file=resp.json()
        with open("sample.json", "w") as outfile:
            json.dump(file, outfile)
        file_json = "sample.json"
        with open(file_json, "r") as json_file:
            data = json.load(json_file)
        j = 1
        place = []
        for i in data["features"]:
            if i["properties"]["country"] == "Peru":
                formato = i["properties"]["formatted"]
                print(f"Sugerencia número {j}°: {formato}")
                j = j + 1
                place.append(formato)
        suge = int(input("Introducir el número de sugerencia: "))
        print("Punto de inicio: ", place[suge-1])
        return place[suge-1]

    def busqueda_destino():
        lugar=input("Intoducir lugar de destino: ")
        resp=api_search(lugar)
        file=resp.json()
        with open("sample2.json", "w") as outfile:
            json.dump(file, outfile)
        file_json = "sample2.json"
        with open(file_json, "r") as json_file:
            data = json.load(json_file)
        j = 1
        place = []
        for i in data["features"]:
            if i["properties"]["country"] == "Peru":
                formato = i["properties"]["formatted"]
                print(f"Sugerencia número {j}°: {formato}")
                j = j + 1
                place.append(formato)
        suge = int(input("Introducir el número de sugerencia: "))
        print("Punto de destino: ", place[suge-1])
        return place[suge-1]
    
def api_search(lugar):
        # url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={lugar}&apiKey=3af67dc42b274747bde3dcf9528d79b8"
        # headers = CaseInsensitiveDict()
        # headers["Accept"] = "application/json"
        # resp = requests.get(url, headers=headers)
        # return resp
        pass
