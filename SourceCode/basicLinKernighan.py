# Umgesetzt in Python 3.8; Grundaufbau gleich zu Implementation von Arthur Matheo

# import der notwendigen externen Pakete
from abc import ABCMeta, abstractmethod
from copy import deepcopy
import math
import numpy as np
import random

# Definierung der TSP Klasse - speichert ein TSP Instanz
class TSP():

    __metaclass__ = ABCMeta

    angles = [[[-1 for i in range(101)]for j in range(101)]for k in range(101)]

    edges = {}  # globale Kostenmatrix
    routes = {}  # globale Kosten der abgespeicherten Rundwege

    # Initialiserung einer TSP Instanz anhand der gegebenen Punkte
    def __init__(self, nodes, fast=False):

        self.nodes = nodes
        self.fast = fast

        self.initial_path = list(nodes)
        # random.shuffle(self.initial_path)
        self.initial_cost = self.pathCost(self.initial_path)
        self.heuristic_path = self.initial_path
        self.heuristic_cost = self.initial_cost

    # Funktion, die einen gegebenen Weg mit seinen Kosten abspeichert
    def save(self, path, cost):

        self.heuristic_path = path
        self.heuristic_cost = cost

        self.routes[str(sorted(path))] = {"path": path, "cost": cost}

    # Funktion, die die strukturierte Ausagbe einer Tour ermöglicht
    def __str__(self):
        out = "Route with {} nodes ({}):\n".format(
            len(self.heuristic_path), self.heuristic_cost)

        if self.heuristic_cost > 0:
            out += " -> ".join(map(str, self.heuristic_path))
            out += " -> {}".format(self.heuristic_path[0])
        else:
            out += "No current route."

        return out

    # Funktion die aus der Kostenmatrix die Entfernung zweier Punkte nimmt
    @staticmethod
    def dist(i, j):
        return TSP.edges[i][j]

    # Funktion, die die Kosten eines Rundweges, inklusiv des Penalties berechnet
    @staticmethod
    def pathCost(path):

        cost = 0

        for i in range(len(path)):
            if i > 2:
                a = calcAngle(coords[path[i-2]], coords[path[i-1]], coords[path[i]]) # Berechnung des Innenwinkels
                if a < 90 and a != 0:
                    cost += 100 * (90 - a) # Verhundertfachung der Differenz zu 90 - hat sich als gute Verrechnung herausgestellt
            cost += TSP.dist(path[i - 1], path[i])

        return cost

    # Initialisierungsfunktion für die Wegkanten
    @staticmethod
    def setEdges(edges):
        TSP.edges = edges

    # Funktion, die die Lösungsfunktion aufruft, welche einen gegebenen Weg optimiert
    def optimise(self):

        route = str(sorted(self.heuristic_path))

        if route in self.routes:
            saved = TSP.routes[route]
            self.heuristic_path = saved["path"]
            self.heuristic_cost = saved["cost"]
        else:
            self._optimise()

        print(self.initial_cost)
        print(list(self.initial_path))

        return self.heuristic_path, self.heuristic_cost

    @abstractmethod
    def _optimise(self):
        pass

# Funktion, die die Knotenreihenfolge für eine Kante wiedergibt
def makePair(i, j):
    if i > j:
        return (j, i)
    else:
        return (i, j)

# Funktion, die mithilfe des Dotproducts und des Arkus Kosinus den Innenwinkel berechnet
def calcAngle(a1, b1, c1):
    a = np.array(a1)
    b = np.array(b1)
    c = np.array(c1)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc)) # Dotproduct
    angle = np.arccos(cosine_angle) # Arkus Kosinus

    res = np.degrees(angle)

    return res

# Klasse, die einen Rundweg repräsentiert
class Tour():

    # Initialiserung eines Rundweges
    def __init__(self, tour):
        self.tour = tour
        self.size = len(tour)
        self.length = TSP.pathCost(tour)
        self._makeEdges()

    # Funktion, die die Liste an Kanten für den aktuellen Rundweg initialisiert
    def _makeEdges(self):
        self.edges = set()

        for i in range(self.size):
            self.edges.add(makePair(self.tour[i - 1], self.tour[i]))

    # Funktion, die den Knoten an einem Index wiedergibt
    def at(self, i):
        return self.tour[i]

    # Funktion, die prüft, ob eine Kante teil eines Rundwegs ist
    def contains(self, edge):
        return edge in self.edges

    # Funktion, die mit Hilfe der calcAngle Funktion und der oben genannten Verrechnungsvorschrift den Penalty von drei Punkten berechnet
    def penalty(self, p, i, s):

        if p == 0 or i == 0 or s == 0: return 0

        if TSP.angles[p][i][s] != -1:
            angle = TSP.angles[p][i][s] 
        else:
            angle = calcAngle(coords[p], coords[i], coords[s])
            TSP.angles[p][i][s] = angle

        if angle < 90 and angle != 0:
            return 100 * (90 - angle)

        return 0

    # Funktion, die den Index eines Punktes in dem Rundweg wiedergibt
    def index(self, i):
        return self.tour.index(i)

    # Funktion, die die beiden Knoten vor und nach einem Punkt wiedergibt
    def around(self, node):
        index = self.tour.index(node)

        pred = index - 1
        succ = index + 1

        if succ == self.size:
            succ = 0

        return (self.tour[pred], self.tour[succ])

    # Funktion, die abhängig von dem prev Parameter entweder Vorgänger oder Nachfolger eines Punktes in dem Rundweg wiedergibt
    def pred(self, index, prev):
        return self.tour[index - 1] if prev else self.tour[index + 1]

    # Funktion, die die Veränderung an dem Rundweg anhand dem derzeitigen alternierenden Spaziergang vornimmt
    def generate(self, broken, joined):
      
        edges = (self.edges - broken) | joined

        # Wenn zu wenige Kanten vorliegen kann kein Rundweg geformt werden
        if len(edges) < self.size:
            return False, []

        successors = {}
        node = 0

        # Aktualisierung der Nachfolger
        while len(edges) > 0:
            for i, j in edges:
                if i == node:
                    successors[node] = j
                    node = j
                    break
                elif j == node:
                    successors[node] = i
                    node = i
                    break

            edges.remove((i, j))

        # jeder Punkt muss einen Nachfolger haben
        if len(successors) < self.size:
            return False, []

        succ = successors[0]
        new_tour = [0]
        visited = set(new_tour)

        while succ not in visited:
            visited.add(succ)
            new_tour.append(succ)
            succ = successors[succ]

        # Der rundweg darf keine Schleife in sich haben
        return len(new_tour) == self.size, new_tour

# Klasse die einen gegebenen Rundweg optimiert
class KOpt(TSP):

    # Funktion, die immer wieder aufgerufen wird, um einen Rundweg zu optimieren
    def _optimise(self):

        better = True
        self.solutions = set()

        # Aufbau der Nachbarlisten
        self.neighbours = {}

        for i in self.heuristic_path:
            self.neighbours[i] = []

            for j, dist in enumerate(TSP.edges[i]):
                if dist > -1 and j in self.heuristic_path: 
                    self.neighbours[i].append(j)

        # Wiederholen, solange eine verbessernde Bewegung gefunden wurde
        while better:
            better = self.improve()
            
            self.solutions.add(str(self.heuristic_path))

        self.save(self.heuristic_path, self.heuristic_cost)

    # Funktion, die anhand der eingegeben Parameter die nähesten Punkte zu einem Punkt berechnet und zusätzlich dafür bereits den gain berechnet
    def closest(self, t1, t2i, tour, gain, broken, joined):

        neighbours = {}

        # Erstellen der Nachbarn von t2i
        for node in self.neighbours[t2i]:
            yi = makePair(t2i, node)

            if yi in broken or tour.contains(yi):
                continue

            NOTt1, option2 = tour.around(t2i)

            if NOTt1 == t1: NOTt1 = option2

            # Berechnung des neuen Gains
            Gi = gain - (TSP.dist(t2i, node) + tour.penalty(NOTt1, t2i, node))

            # jede neue Kante muss eine positiven Gain haben, nicht schon entfernt werden sollen und nicht zum Rundweg gehören
            if Gi <= 0:
                continue

            aroundNode = tour.around(node)
            NOTsuccIdx = 0

            for succ in aroundNode:

                NOTsucc = aroundNode[1 - NOTsuccIdx]
                NOTsuccIdx = 1

                xi = makePair(node, succ)

                # prüfen, dass Kante nicht bereits entfernt oder hinzugefügt werden soll
                if xi not in broken and xi not in joined:

                    NOTnode, option22 = tour.around(NOTsucc)

                    if NOTnode == node: NOTnode = option22

                    diff = (TSP.dist(node, succ) + tour.penalty(node, NOTsucc, NOTnode)) - (TSP.dist(t2i, node) + tour.penalty(NOTt1, t2i, node))
                    Gi -= tour.penalty(t2i, node, NOTsucc)

                    if node in neighbours and diff > neighbours[node][0]:
                        neighbours[node][0] = diff
                    else:
                        neighbours[node] = [diff, Gi]

        # Rückgabe der Nachbarn sortiert nach möglichem Gain
        return sorted(neighbours.items(), key=lambda x: x[1][0], reverse=True)

    # Funktion, die den Algorithmus mit dem aktuellen Rundweg startet
    def improve(self):

        tour = Tour(self.heuristic_path)

        # die ersten vier Kanten symbolisieren das Ausprobieren aller 2-opt-moves
        for t1 in self.heuristic_path:
            around = tour.around(t1)

            NOTt2Idx = 0

            for t2 in around:
                broken = set([makePair(t1, t2)])

                NOTt2 = around[1 - NOTt2Idx]
                NOTt2Idx = 1

                NOTt1, option2 = tour.around(t2)

                if NOTt1 == t1: NOTt1 = option2

                # gain, wenn erste Kante entfernt werden würde
                gain = (TSP.dist(t1, t2) + tour.penalty(NOTt2, t1, t2) + tour.penalty(t1, t2, NOTt1)) 

                close = self.closest(t1, t2, tour, gain, broken, set())

                # die 5 vielversprechendsten Nachbarn werden probiert
                tries = 5

                for t3, (_, Gi) in close:

                    # darf nicht schon zum Rundweg gehören
                    if t3 in around:
                        continue

                    joined = set([makePair(t2, t3)])

                    # wenn verbessernde Bewegung gefunden wurde, zurück zur Hauptschleife
                    if self.chooseX(tour, t1, t2, t3, t2, Gi, broken, joined):
                        return True

                    # Sonst noch die weiteren Optionen probieren

                    tries -= 1
                    if tries == 0:
                        break

        return False

    # Funktion, die eine (weitere) Kante wählt, die entfernt werden soll
    def chooseX(self, tour, t1, t2, last, bef, gain, broken, joined):

        around = tour.around(last)

        NOTt2iIdx = 0

        for t2i in around:
            xi = makePair(last, t2i)

            NOTt2i = around[1 - NOTt2iIdx]
            NOTt2iIdx = 1

            NOTlast, option2 = tour.around(t2i)
            if NOTlast == last: NOTlast = option2

            # Gain bei aktuellen Iteration
            Gi = gain + (TSP.dist(last, t2i) + tour.penalty(NOTt2i, last, t2i) + tour.penalty(NOTlast, t2i, last))

            if xi not in joined and xi not in broken:
                added = deepcopy(joined)
                removed = deepcopy(broken)

                # Prüfen, ob der Rundweg nun wieder mit dem Spaziergang aktualisiert werden kann, d.h. dieser geschlossen ist

                removed.add(xi)
                added.add(makePair(t2i, t1)) 

                NOTt2, option22 = tour.around(t1)
                if NOTt2 == t2: NOTt2 = option22

                if t2i == t1: 
                    continue

                is_tour, new_tour = tour.generate(removed, added)

                # Prüfen, ob ein valider Rundweg vorliegt
                if not is_tour and len(added) > 2:
                    continue

                # Abbruch, falls es die Lösung schonmal gab
                if str(new_tour) in self.solutions:
                    return False

                relink = Gi - (TSP.dist(t2i, t1) + tour.penalty(t1, t2i, NOTlast) + tour.penalty(NOTt2, t1, t2i))

                newCost = TSP.pathCost(new_tour)

                # prüfen, dass dieser neue Rundweg ein Rundweg ist und besser ist als der alte
                if is_tour and relink > 0:

                    # Aktualisieren der Werte
                    self.heuristic_path = new_tour
                    self.heuristic_cost = newCost 

                    return True
                else:
                    # Sonst wird ohne den Wiederverbindungsteil der Spaziergang weiter verlängert
                    choice = self.chooseY(tour, t1, t2, last, t2i, Gi, removed, joined)

                    if len(broken) == 2 and choice:
                        return True
                    else:
                        return choice

        return False

    # wählt analog zu chooseX eine Kante zum Hinzufügen zu dem Rundweg
    def chooseY(self, tour, t1, t2, bef, t2i, gain, broken, joined):
        
        ordered = self.closest(bef, t2i, tour, gain, broken, joined)

        # wenn i = 2 ist, dann fünf vielversprechendsten, sonst nur den vielversprechendsten
        if len(broken) == 2:
            top = 5
        else:
            top = 1

        for node, (_, Gi) in ordered:
            yi = makePair(t2i, node)
            added = deepcopy(joined)
            added.add(yi)

            # Sobald eine verbessernde Bewegung gefunden wurde, aufhören
            if self.chooseX(tour, t1, t2, node, t2i, Gi, broken, added):
                return True

            top -= 1
            if top == 0:
                return False

        return False

# Funktion, die den Abstand zweier Punkte berechnet
def distBetween(i, j):
    return math.sqrt((pow(abs(j[0] - i[0]), 2) + pow(abs(j[1] - i[1]), 2)) * 1.0);

# Funktion, die ursprünglich die Kostenmatrix erstellt
def constructMatrix(coords):
    matrix = [[-1 for i in range(len(coords))] for j in range(len(coords))] # Initialisierung der Matrix

    for i in range(len(coords)):
        for j in range(len(coords)):

            if i == j: continue
            if i > j: continue

            d = distBetween(coords[i], coords[j]) # Berechnung der Abstände

            # Speicherung der Abstände
            matrix[i][j] = d
            matrix[j][i] = d

    for arr in matrix:
        arr.insert(0, 0)

    matrix.insert(0, [0 for i in range(len(coords)+1)])
    matrix[0][0] = -1

    return matrix

# main-Funktion
if __name__ == "__main__":

    # Einlesen der Daten
    coords = []
    with open('input.txt') as file:

        for l in file:
            row = l.split()
            coords.append((float(row[0]), float(row[1])))

    # Erstellen der Kostenmatrix
    matrix = constructMatrix(coords)
    coords.insert(0, (0, 0))

    # TSP Instanz initialisieren
    TSP.setEdges(matrix)
    lk = KOpt(range(len(matrix)))

    # Lösungsfunktion aufrufen und beste Lösung ausgeben
    for _ in range(2):
        path, cost = lk.optimise()
        print("Best path has cost: {}".format(cost))
        print([i - 1 for i in path[1:]])
