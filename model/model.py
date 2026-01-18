import networkx as nx
from database.dao import DAO
from geopy import distance
from operator import itemgetter


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.state_dict = {}

    def fill_dd_year(self):
        anni = DAO.get_year()
        return anni
    def fill_dd_shape(self,year):
        shape = DAO.get_shape(year)
        return shape
    def build_graph(self,shape,year):
        self.G.clear()
        nodi = DAO.get_states()
        for state in nodi:
            self.state_dict[state.id] = state
            self.G.add_node(state)
        connessioni = DAO.get_connessioni()
        tratte_uniche = {}
        for c in connessioni:
            key = tuple(sorted(c))
            if key not in tratte_uniche:
                tratte_uniche[key] = c
        connessioni_uniche = list(tratte_uniche.values())
        for v, u in connessioni_uniche:
            v_nodo = self.state_dict[v]
            u_nodo = self.state_dict[u]
            peso1 = DAO.get_peso_nodo(str(shape),float(year),str(v))
            peso2 = DAO.get_peso_nodo(str(shape),float(year),str(u))
            peso_arco = peso1 + peso2
            if peso_arco != 0:
                self.G.add_edge(v_nodo,u_nodo, peso=peso_arco)
        nodo_somma = {}
        for v in self.G.nodes():
            somma_pesi_arco = 0
            for n in self.G.neighbors(v):
                somma_pesi_arco += self.G[v][n]['peso']
            nodo_somma[v.id] = somma_pesi_arco

        return nodo_somma, self.G.number_of_nodes(), self.G.number_of_edges()

    def percorso(self):
        self.best_path = [] # arco - peso - distanza tra u e v dell'arco
        self.best_distance = 0 # distanzaTot distenze arco

        for source in self.G.nodes():
            path_corrente= []
            distance_corrente = 0
            peso_ultimo_arco = float('-inf')
            archi_visitati = set()

            vicini = self.get_vicini_ordinati(source)

            for vicino, peso_arco in vicini:

                if (source.id, vicino.id) not in archi_visitati and (peso_arco > peso_ultimo_arco):
                    archi_visitati.add((source.id, vicino.id))
                    d = distance.geodesic((source.lat, source.lng), (vicino.lat, vicino.lng)).km
                    path_corrente.append(((source.id, vicino.id), peso_arco, d))
                    self.ricorsione_percorso(vicino,path_corrente, archi_visitati, peso_arco, distance_corrente + d)

                    path_corrente.pop()
                    archi_visitati.remove((source.id, vicino.id))

        return self.best_path, self.best_distance

    def ricorsione_percorso(self, ultimo_nodo, path_corrente, archi_visitati, peso_ultimo_arco, distance_corrente):

        if distance_corrente > self.best_distance:
            self.best_distance = distance_corrente
            self.best_path = list(path_corrente)

        vicini = self.get_vicini_ordinati(ultimo_nodo)

        for vicino, peso_arco in vicini:

            if (ultimo_nodo.id, vicino.id) not in archi_visitati and (peso_arco > peso_ultimo_arco):

                archi_visitati.add((ultimo_nodo.id, vicino.id))
                d = distance.geodesic((ultimo_nodo.lat, ultimo_nodo.lng), (vicino.lat, vicino.lng)).km
                path_corrente.append(((ultimo_nodo.id, vicino.id), peso_arco, d))

                self.ricorsione_percorso(vicino, path_corrente, archi_visitati, peso_arco, distance_corrente + d)

                path_corrente.pop()
                archi_visitati.remove((ultimo_nodo.id, vicino.id))

    def get_vicini_ordinati(self, nodo):
        lista_vicini = []
        for vicino in self.G.neighbors(nodo):
            peso = self.G[nodo][vicino]['peso']
            lista_vicini.append((vicino, peso))
        return sorted(lista_vicini, key=itemgetter(1))
