from random import sample, randint

def get_rec_info():
    # esta funcion retorna una lista con tuplas de la frecuencia y la frase asociada y
    # tambien una lista de prefijos asociada, para la cual deberian poder dar una 
    # recomendacion en menos de 1.5 segundos (en colab).
    # es importante que el archivo 'info_recomendaciones.txt' este el la misma carpeta que
    # el script. En colab se pueden subir archivos con el navegador en la izquierda. 

    with open('info_recomendaciones.txt', 'r') as file:
        ret = [(int(line[0]), ' '.join(line[2:])) for line in [l.strip().split() for l in file]]
    prefijos = sample(list(set(pal[:randint(1,9*len(pal)//10)] for pal in [p[1] for p in ret])), 3000)
    return ret, prefijos

frecuencias, prefijos = get_rec_info()

print(frecuencias, prefijos)
