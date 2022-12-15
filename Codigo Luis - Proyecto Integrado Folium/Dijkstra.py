class Vertice:

    def __init__(self,id):
        self.id = id
        self.visitado = False
        self.distancia = float('inf')
        self.padre = None
        self.vecinos = []

    def agregar_vecinos(self,v,p):
        if v not in self.vecinos:
            self.vecinos.append([v,p])

class Grafo:

    def __init__(self):
        self.vertice = {}

    def agregar_vertice(self,v):
        if v not in self.vertice:
            self.vertice[v] = Vertice(v)

    def agregar_aristas(self,a,b,d):
        if a in self.vertice and b in self.vertice:
            self.vertice[a].agregar_vecinos(b,d)
            self.vertice[b].agregar_vecinos(a,d)

    def imprimir(self):
        for v in self.vertice:
            print('La distancia del vértice ' +str(v)+' es '+str(self.vertice[v].distancia)+' llegando desde '+str(self.vertice[v].padre))

    def caminos(self,a,b):
        caminos = []
        actual = b
        while actual != None:
            caminos.insert(0,actual)
            actual = self.vertice[actual].padre
        return [caminos, self.vertice[b].distancia]

    def menor_peso(self,lista):
        if len(lista) >0:
            menor = self.vertice[lista[0]].distancia
            v = lista[0]
            for e in lista:
                if menor > self.vertice[e].distancia:
                    menor = self.vertice[e].distancia
                    v = e
            return v

    def dijkstra(self,a):
        if a in self.vertice:
            self.vertice[a].distancia=0
            inicial = a
            no_visitados = []
            for v in self.vertice:
                if v != inicial:
                    self.vertice[v].distancia = float('inf')
                self.vertice[v].padre = None
                no_visitados.append(v)
            while len(no_visitados)>0:
                for vecino in self.vertice[inicial].vecinos:
                    if not self.vertice[vecino[0]].visitado:
                        if self.vertice[inicial].distancia + vecino[1] < self.vertice[vecino[0]].distancia:
                            self.vertice[vecino[0]].distancia = self.vertice[inicial].distancia + vecino[1]
                            self.vertice[vecino[0]].padre = inicial
                self.vertice[inicial].visitado = True
                no_visitados.remove(inicial)
                inicial = self.menor_peso(no_visitados)
        else:
            return False

class display_dijkstra():
    def main():
        g = Grafo()
        Ciudades = ['Lima', 'Trujillo', 'Ica', 'Piura', 'Cuzco', 'Arequipa']

        for i in Ciudades:
            g.agregar_vertice(i)

        g.agregar_aristas('Lima', 'Arequipa', 14)
        g.agregar_aristas('Lima', 'Trujillo', 7)
        g.agregar_aristas('Lima', 'Ica', 9)
        g.agregar_aristas('Trujillo', 'Ica', 10)
        g.agregar_aristas('Trujillo', 'Piura', 15)
        g.agregar_aristas('Ica', 'Piura', 11)
        g.agregar_aristas('Ica', 'Arequipa', 2)
        g.agregar_aristas('Piura', 'Cuzco', 6)
        g.agregar_aristas('Cuzco', 'Arequipa', 9)

        g.dijkstra('Lima')
        print('El camino mas corto es:')
        print(g.caminos('Lima','Arequipa'))
        g.imprimir()
