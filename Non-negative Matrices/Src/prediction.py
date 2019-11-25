from sklearn.metrics    import pairwise 
from sklearn.neighbors import KDTree

import numpy as np
from numpy import linalg

VIOLIN   = ("../audios/violin/retocadas", [], ["trill"], "violin")
FLAUTA   = ("../audios/flauta/retocadas", [], ["trill"], "flauta")
GUITARRA = ("../audios/guitar/retocadas", [], ["trill"], "guitarra")


def cosine_similarity(a, b):
	arriba = a.T.dot(b)
	abajo  = linalg.norm(a) * linalg.norm(b)

	return arriba / abajo  

# Usamos Cosine Similarity Measure para knn
def k_near_neighbors(predicted, acts):
    max_label     = 0
    max_label_val = -1

    for i in range(acts.shape[0]):
        current = cosine_similarity(predicted, acts[i])

        if current > max_label_val:
           max_label     = i
           max_label_val = current

    return max_label
    # Pred -> 33, 6237
    # acts -> 3, 6237

def predict(dataset, test_file_path):
    comps_inv, acts = dataset
    test = get_audio_features(test_file_path)

    # Generamos la prediccion de test 
    W = comps_inv
    test_vect = test

    # Para sacar el nuevo vector de activaciones calculamos
    # Componentes^(-1) * test_vect_features = activacion_test
    predicted = W.dot(test_vect)

    # Calculamos el instrumento mas cercano al de test
    pred = k_near_neighbors(predicted, acts)
    print(pred)
    return pred

instruments = [VIOLIN, FLAUTA, GUITARRA]
comps_inv, acts = generate_dataset(instruments=instruments)
# generate_dataset("audios/violin", ["arco", "normal", "pianissimo"], ["trill"], "violin")
# generate_dataset("audios/clash cymbals", [], ["trill"], "clas_symbals")3
# generate_dataset("audios/flute", ["fortissimo", "normal"], ["trill"], "flute")