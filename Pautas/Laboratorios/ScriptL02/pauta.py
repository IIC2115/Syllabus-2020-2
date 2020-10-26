## pauta.py
### Este archivo es parte del Corrector automatico 
### de entregas de laboratorio desarrollado para el 
### curso IIC2115. Este archivo debe contener:
##### - Soluciones a cada uno de los problemas
##### - Funciones generadores de inputs
##### - Funciones de verificacion de respuesta correcta
### Francisco Garrido-Valenzuela 2020
import random # no borrar

# FORMATOS:
## Todo lo qu este entre [], debe ser modificado en cada caso

## SOLUCIONES
### def [nombre_problema](input1, input2, ..., inputn):
###     # solucion
###     return resp

## INPUTS
### def inputs_[problem_code](size, seed):
###     # generacion
###     return [input1, input2, ..., inputn]

## VERIFICADORES
### def verificar_[problem_code](resp, inputs)
###     correcta = [nombre_problema](*inputs)
###         if resp == correcta:
###             return 1
###         else:
###             return 0

####################
#### SOLUCIONES ####
####################

# Imports necesarios en solucion de problemas

######## Problema 1a ########
def save_sword(key:str, espadas:list) -> list:
    espadas[ord(key)-97] += 1
    return espadas

def derrotar_bestia(lock:str, espadas:list) -> tuple:
    i = ord(lock)-65
    if espadas[i] > 0:
        espadas[i] -= 1
        return True, espadas
    return False, espadas

def numero_espadas(mapa:str) -> bool:
    espadas = [0]*26
    buy = 0

    for i in range(0,len(mapa),2):
        i, j = i, i+1
        espadas = save_sword(mapa[i], espadas)
        derrotar, espadas = derrotar_bestia(mapa[j], espadas)
        if not derrotar: # si no puedo derrotar a la bestia compro una espada
            buy += 1
    return buy
#############################

######## Problema 2a ######## 
from random import randint
from itertools import count
from heapq import heappop, heappush
import math
from collections import defaultdict

class Heap:
    # codigo extraido de https://docs.python.org/3/library/heapq.html
    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = count()               # unique sequence count
        
    def add(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)
    
    def remove(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
        
    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            _, _, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def lenght(self):
        return len([x for x in self.pq if x[2] != self.REMOVED])

    def contains(self, task):
        return task in self.entry_finder

    def empty(self):
        return self.lenght() == 0

    def show(self):
        lista = [(x[2][:2], x[0]) for x in self.pq if 'removed' not in x[2]]
        lista = sorted(lista, key=lambda x: x[1])
        return lista

def h(tablero:list, i:int, j:int, p:int, q:int) -> int:
    # heuristica, distancia euclidiana + diferencia de altura
    her = int(math.sqrt(abs(i-p)**2 + abs(j-q)**2)) # int trunca el numero
    # obtengo la alturas
    a1, a2 = tablero[i][j],  tablero[p][q]
    if a1 < a2:
        her += a2 - a1
    return her

def opciones(i:int, j:int, alto:int, ancho:int) -> list:
    ret = []
    # reviso las 8 opciones de posiciones
    # si estan dentro del tablero las retorno en ret
    for p in [i-1, i, i+1]:
        if 0 <= p < alto:
            for q in [j-1, j, j+1]:
                if 0 <= q < ancho:
                    ret.append((p, q))
    return ret

def new_g(tablero:list, g:dict, i:int, j:int, x:int, y:int) -> int:
    # distancia recorrida desde el inicio hasta (x, y) 
    # mas el costo de pasar de (x, y) a (i,j)
    d = g[(x, y)] + 1 
    d += abs(tablero[i][j] - tablero[x][y]) if tablero[i][j] > tablero[x][y] else 0
    return d

def get_inf() -> int:
    return math.inf


def astar(tablero:list, i:int, j:int, p:int, q:int, verbosidad=False) -> tuple:
    #posicion de inicio y final
    inicio = (i, j)
    final = (p, q)

    #lista de pos por revisar
    open_list = Heap()
    #set de pos ya visitadas
    close_list = set()
    # diccionario de el mejor nodo visitado anterior a la llave
    previous = {}
    # diccionario de la menor distancia recorrida del inicio a cada nodo
    g = defaultdict(get_inf)
    # diccionario con la mejor estimacion del mejor camino pasando por este nodo
    f = defaultdict(get_inf)

    previous[inicio] = inicio
    g[inicio] = 0
    f[inicio] = h(tablero, i, j, p, q)

    alto = len(tablero)
    ancho = len(tablero[0])

    # agrego la posicion de inicio a los nodo por revisar
    open_list.add(inicio, f[inicio])

    # mientras existan nodos a revisar sigo buscando
    while not open_list.empty():
        # elijo el nodo con menor f
        i, j = open_list.pop()       
        
        close_list.add((i, j))

        # si llego al final dejo de buscar
        if (i, j) == final:
            break

        # busco todas las nuevas opciones y las agrego a la lista de abierto
        for pos in opciones(i, j, alto, ancho):
            
            a, b = pos    
            sig_g = new_g(tablero, g, a, b, i, j)
            sig_f = sig_g+h(tablero, a, b, p, q)

            # reviso si vale la pena revisar el nodo
            if f[pos] <= sig_f:
                if open_list.contains(pos):
                    continue
                if pos in close_list:
                    continue

            if pos in close_list:
                close_list.remove(pos)
            
            # setea el nodo anterior
            previous[pos] = (i,j)
            # reemplaza anterior g
            g[pos] = sig_g
            # reemplaza anterior f
            f[pos] = sig_f
            
            open_list.add(pos, f[pos])

    # reviso si logre llegar a mi destino
    if final not in previous:
        return ([], math.inf, len(close_list)) if verbosidad else ([], math.inf)
    else:
        camino = []
        actual = final
        dist_tot = g[actual]

        while inicio != previous[actual]:
            camino.insert(0, actual)
            actual = previous[actual]
        
        camino.insert(0, actual)
        camino.insert(0, inicio)
        return (camino, dist_tot, len(close_list)) if verbosidad else (camino, dist_tot)

def dijkstra(tablero:list, i:int, j:int, p:int, q:int, verbosidad=False) -> tuple:
    #posicion de inicio y final
    inicio = (i, j)
    final = (p, q)

    #lista de pos por revisar
    open_list = Heap()
    #set de pos ya visitadas
    close_list = set()

    # diccionario de el mejor nodo visitado anterior a la llave
    previous = {}
    # diccionario de la menor distancia recorrida del inicio a cada nodo
    g = defaultdict(get_inf)

    previous[inicio] = inicio
    g[inicio] = 0

    alto = len(tablero)
    ancho = len(tablero[0])

    # agrego la posicion de inicio a los nodo por revisar
    open_list.add(inicio, 1)

    # mientras existan nodos a revisar sigo buscando
    while not open_list.empty():
        # elijo el nodo con menor f
        i, j = open_list.pop()     
        close_list.add((i,j))
        # busco todas las nuevas opciones y las agrego a la lista de abierto
        for pos in opciones(i, j, alto, ancho):
            if pos in close_list:
                continue
            a, b = pos    
            sig_g = new_g(tablero, g, a, b, i, j)

            # reviso si vale la pena actualizar distancias
            if sig_g < g[pos]:
                # setea el nodo anterior
                previous[pos] = (i,j)
                # reemplaza anterior g
                g[pos] = sig_g
                open_list.add(pos, g[pos])

    camino = []
    actual = final
    dist_tot = g[actual]

    while inicio != previous[actual]:
        camino.insert(0, actual)
        actual = previous[actual]
    
    camino.insert(0, actual)
    camino.insert(0, inicio)
    return (camino, dist_tot, alto*ancho) if verbosidad else (camino, dist_tot)

def ruta_de_jaime(origen, destino, mapa, metodo = "astar"):
    # El problema debiera resolverse con A estrella, pero de todas formas se muestra una solución utilizando Dijkstra también
    metodos = {"astar": astar, "dijkstra": dijkstra}
    return metodos[metodo](mapa,*origen,*destino)
#############################

######## Problema 2b ########
from random import sample, randint

class Nodo:
    def __init__(self):
        self.terminal:bool = False
        self.hoja:bool = True
        self.cantidad:int = 0
        self.frase:str = ''
        self.hijos:dict = {}

    def agregar(self, frase: str, cantidad: int, index: int=0):
        if len(frase) == index:
            self.frase = frase
            self.cantidad = cantidad
            self.terminal = True
            return

        self.hoja = False
        letra = frase[index]

        if letra not in self.hijos:
            self.hijos[letra] = Nodo()

        self.hijos[letra].agregar(frase, cantidad, index+1)

    def cant_pal(self) -> tuple:
        return (self.cantidad, self.frase)

    def buscar_recomendacion(self) -> list:
        open_queue = list(self.hijos.keys())
        recomendaciones = []
        for opcion in open_queue:
            if self.hijos[opcion].terminal:
                recomendaciones.append(self.hijos[opcion].cant_pal())
            recomendaciones.extend(self.hijos[opcion].buscar_recomendacion())

        if len(recomendaciones) > 0:
            recomendaciones = sorted(recomendaciones, key=lambda x: x[0], reverse=True)

            return recomendaciones[0:1]
        return []

    def recomendar(self, frase: str) -> str:
        if len(frase) == 0:
            opciones = self.buscar_recomendacion()
            if len(opciones) == 0:
                return ''
            return opciones[0][1]

        letra, frase = frase[0], frase[1:]

        # si no encuento la frase retorno un str vacio
        if letra not in self.hijos:
            return ''

        return self.hijos[letra].recomendar(frase)

def motor_lobel(prefijos, historico):
    recomendaciones = []
    trie = Nodo()
    for line in historico:
        cantidad, frase = line
        trie.agregar(frase, cantidad)
    for prefijo in prefijos:
        recomendaciones.append(trie.recomendar(prefijo))

    return recomendaciones # Debe ser una lista de strings
#############################

######## Problema 3a ########
# i es el largo del string revisado hasta el momento
# j es el largo del patron hasta el momento
def r_solve(string:str, i:int, pat:str, j:int, dicto:dict) -> bool:
    n = len(string)
    m = len(pat)

    # Caso base: No puedo tener un string con menos caracteres que el patron restante
    if n < m:
        return False

    # revise todo el string y ocupe todo el patron, encontre una solucion
    if i == n and j == m:
        return True

    # si ya termine con el string o el patron y aun me queda del otro, esta no era la solucion
    if i == n or j == m:
        return False

    # reviso la siguiente letra del patron
    curr = pat[j]

    # si ya he visto esta letra antes, continuo con su valor asignado
    if curr in dicto:

        # obtengo el string asignado a la letra actual del patron
        s = dicto[curr]
        k = len(s)

        # obtengo los siguientes k caracteres del string, partiendo desde el indice i.
        if i + k < len(string):
            ss = string[i:i + k]
        else:
            ss = string[i:]

        # retorno falso si el substring obtenido es diferente al almacenado anteriormente
        if ss != s:
            return False

        # en caso de que si calzara sigo buscando en la siguiente letra del patron y avanzando k indices en el string
        return r_solve(string, i + k, pat, j + 1, dicto)

    # si nunca he visto el caracter del patron
    # reviso que sea de largo, desde 1, hasta la cantidad restante de caracteres en el string
    for k in range(1, n - i + 1):

        # agrego al diccionario el substring con los siguientes k caracteres del string
        dicto[curr] = string[i:i + k]

        # reviso si es una posible solucion
        if r_solve(string, i + k, pat, j + 1, dicto):
            return True

        # else: backtrack - lo elimino y reviso con un subtring de largo k+=1
        dicto.pop(curr)

    return False

def traduccion(mensaje, estructura):
    respuesta = dict()
    r_solve(mensaje, 0, estructura.replace(" ",""), 0, respuesta)
    return tuple((key, value) for key,value in respuesta.items()) # Debe ser una tupla de tuplas
#############################

################
#### INPUTS ####
################

def in_p1a(n=10):
    minusculas = 'abcdefghijklmnoprstuvwxyz'[:]
    mayusculas = minusculas.upper()
    n = n # el largo del problema = 2*n
    minn = [random.sample(minusculas, 1)[0] for _ in range(n)]
    mayy = [random.sample(mayusculas, 1)[0] for _ in range(n)]
    return ''.join([minn[i] + mayy[i] for i in range(n)])

def inputs_p1a(size, seed):
    if size == 1:
        n = 20
    elif size == 2:
        n = 10000
    else:
        n = 200000
    random.seed(seed)
    return [in_p1a(n)]

def in_p2a(h, n):
    tablero = [[randint(1,h) for x in range(n)] for _ in range(n)]
    i, j, p, q = 0,0,n-1,n-1 #randint(0, n//2), randint(0, n//2), randint(n//2+1, n-1), randint(n//2+1, n-1)
    return [(i,j), (p,q), tablero]

def inputs_p2a(size, seed):
    if size == 1:
        h = 1000
        n = 10
    elif size == 2:
        h = 1000
        n = 50
    else:
        h = 1000
        n = 100
    random.seed(seed)
    return in_p2a(h, n)

def get_rec_info(n, m): # Esto no es necesario, es solo para leer la base de datos desde el txt
    # esta funcion retorna una lista con tuplas de la frecuencia y la frase asociada y
    # tambien una lista de prefijos asociada, para la cual deberian poder dar una 
    # recomendacion en menos de 1.5 segundos (en colab).
    # es importante que el archivo 'info_recomendaciones.txt' este el la misma carpeta que
    # el script. En colab se pueden subir archivos con el navegador en la izquierda. 

    with open('info_recomendaciones.txt', 'r') as file:
        ret = [(int(line[0]), ' '.join(line[2:])) for line in [l.strip().split() for l in file]][:m]
    prefijos = sample(list(set(pal[:randint(1,9*len(pal)//10)] for pal in [p[1] for p in ret])), n)
    return prefijos, ret

def inputs_p2b(size, seed):
    if size == 1:
        n = 5
        m = 20
    elif size == 2:
        n = 100
        m = 250
    else:
        n = 3000
        m = 5000
    random.seed(seed)
    prefijos, ret = get_rec_info(n, m)
    return [prefijos, ret]   

def regex(L=10, m=4, M=10, n=15, N=15, p=100):
    patron = [chr(randint(0,min(L, 25))+65) for _ in range(randint(m, M))]
    if randint(0, 99) < p:
        dic = {}
        for k in patron:
            dic[k] = ''.join([chr(randint(0,25)+97) for _ in range(1, randint(n, N))])
        str_final = ''.join([dic[k] for k in patron])
    else:
        str_final = ''.join([chr(randint(0,25)+97) for _ in range(1, randint(n*m, N*M))])
    
    patron = ' '.join(patron)
    return str_final, patron

def inputs_p3a(size, seed):
    if size == 1:
        L = 10
        m = 3
        M = 3
        n = 8
        N = 8
        p = 100
    elif size == 2:
        L = 10
        m = 5
        M = 5
        n = 10
        N = 10
        p = 100
    else:
        L = 10
        m = 6
        M = 6
        n = 11
        N = 11
        p = 100
    random.seed(seed)
    mensaje, estructura = regex(L, m, M, n, N, p)
    return [mensaje, estructura]

#######################
#### VERIFICADORES ####
#######################

def verificar_p1a(resp, inputs):
    correcta = numero_espadas(*inputs)
    if resp == correcta:
        return 1
    else:
        return 0

def verificar_p2a(resp, inputs):
    correcta = ruta_de_jaime(*inputs)
    if resp[1] == correcta[1]:
        return 1
    else:
        return 0

def convert(tup, di): 
    for a, b in tup: 
        di.setdefault(b, []).append(a) 
    return di 

def verificar_p2b(resp, inputs):
    correcta = motor_lobel(*inputs)
    prefixs = inputs[0]
    hist = inputs[1]
    hist_dict = {} 
    hist_dict = convert(hist, hist_dict)

    for i, p in enumerate(prefixs):
        if not(p == resp[i][:len(p)] and hist_dict[correcta[i]][0] == hist_dict[resp[i]][0]):
            return 0
    return 1
            

def convert_inv(tup, di): 
    for a, b in tup: 
        di.setdefault(a, []).append(b) 
    return di 

def verificar_p3a(resp, inputs):
    resp_dict = {}
    resp_dict = convert_inv(resp, resp_dict)
    estructura = inputs[1]
    estructura = estructura.replace(' ', '')
    propuesto = ''
    for c in estructura:
        propuesto += resp_dict[c][0]

    if propuesto == inputs[0]:
        return 1
    else:
        return 0