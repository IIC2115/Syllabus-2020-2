def leer_red(archivo):
    
    with open(archivo) as f:
        nodos = []
        arcos = []
        for i, line in enumerate(f):
            if i == 0:
                j = int(line.strip())+1
            
            elif i<j:
                data = line.split(',')
                nodo = (data[0].strip(), int(data[1].strip()))
                nodos.append(nodo)
                
            elif i>j:
                data = line.split(',')
                arco = (data[0].strip(), data[1].strip())
                arcos.append(arco)
        return [nodos, arcos]