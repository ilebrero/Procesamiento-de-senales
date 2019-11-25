from sklearn.metrics   import pairwise 
from sklearn.neighbors import KDTree

import operator
import numpy as np
from numpy import linalg

VIOLIN   = ("../audios/violin/retocadas_MIS", [], ["trill"], "violin")
FLAUTA   = ("../audios/flauta/retocadas_MIS", [], ["trill"], "flauta")
GUITARRA = ("../audios/guitar/retocadas", [], ["trill"], "guitarra")

def cosine_similarity(a, b):
    numerador   = a.T.dot(b)
    denominador = linalg.norm(a) * linalg.norm(b)
    
    return numerador / denominador

def calcular_distancias(H_t, predicted):
    distancias = []
    
    for i in range(H_t.shape[0]):
        distancias.append(
            cosine_similarity(
                predicted, 
                H_t[i]
            )
        )
        
    return distancias


def get_key_from_max_value(dic):
    return max(dic.items(), key=operator.itemgetter(1))[0]

def count_frecuencies(labels_ordenados):
    frecuencias = dict()
    
    for i in range(len(labels_ordenados)):
        val = labels_ordenados[i]
        if val in frecuencias.keys():
            frecuencias[val] = frecuencias[val] + 1
        else:
            frecuencias[val] = 1
            
    return frecuencias

# Usamos Cosine Similarity Measure para knn, probar si anda bien
# predicted tiene shape: #Instr * 1
# H tiene shape: #Instr * #Audios
# h_i columna tiene shape 1 * # instrumentso <- estas comparamos 
def k_near_neighbors(predicted, acts, labels, k):
    max_label     = 0
    max_label_val = -1
    
    H_t = acts.T
    
    # Calculamos las distancias a todo el resto de los audios
    distancias = calcular_distancias(H_t, predicted)
    
    print(np.array(distancias).shape)
    
    # Ordenamos los labels en base a cuales estan mas cerca
    labels_ordenados_por_distancia = [
        label 
        for _,label 
        in sorted(
            zip(distancias,labels),
            reverse=True
        )
    ]
    
    print(labels_ordenados_por_distancia)
    
    # Calculamos las frecuencias de los primeros k labels
    frecuencias = count_frecuencies(
        labels_ordenados_por_distancia[:k]
    )
    
    # Predecimos el label que mas veces aparecio
    predicted_label = get_key_from_max_value(frecuencias)
    return predicted_label
    
def predict(dataset, k, test_file_path):
    comps_inv, acts, labels = dataset
    test = get_audio_features(test_file_path)

    # Generamos la prediccion de test 
    W = comps_inv
    test_vect = test

    # Para sacar el nuevo vector de activaciones calculamos
    # Componentes^(-1) * test_vect_features = activacion_test
    predicted = W.dot(test_vect.T)

    # Calculamos el instrumento mas cercano al de test
    pred = k_near_neighbors(predicted, acts, labels, k)
    return pred
