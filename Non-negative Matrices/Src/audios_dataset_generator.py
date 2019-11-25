import sklearn.decomposition
import librosa

from os import listdir, mkdir
from os.path import isfile, join, splitext, getsize

from numpy import linalg

def concatenate(a, b):
    if a.size == 0: return b
    return np.concatenate((a, b))

def containsAll(substrings, string):
    res = True
    for s in substrings:
        res = res and (s in string)
    return res


def containsAny(substrings, string):
    res = False
    for s in substrings:
        res = res or (s in string)
    return res

def getConcat(arr):
    res = ""
    for a in arr:
        res = res + "_" + a
    return res

def generate_stacked_new_row(a, b):
    if a.size == 0: return b # Caso especial si a no tiene elems todavia
    return np.vstack( (a, b) )


def filter_valid_names(names, substrings, not_substrings):
	res = []

	for name in names:
		if containsAll(substrings, name) and not containsAny(not_substrings, name):
			res.append(name)

	return res

def getFiles(directory, substrings, not_substrings):
    # Pruebo levantar por size
    all_paths = [
        file_path 
            for file_path 
            in listdir(directory) 
                if isfile(join(directory, file_path))
    ]

    all_paths = filter_valid_names(all_paths, substrings, not_substrings)

    return all_paths

def get_audio_features(file_path):
    y, sr = librosa.load(file_path)
    return generate_audio_features(y, sr)

def generate_instrument_dataset(directory, substrings, not_substrings, instrument):
    instrument_dataset = np.array([])
    files = getFiles(directory, substrings, not_substrings)

    # Generamos el instrument_dataset
    for file in files:
        file_path = join(directory, file)

        instrument_dataset = generate_stacked_new_row(
            instrument_dataset, 
            get_audio_features(file_path)
        )
            
    return instrument_dataset

def generate_dataset(instruments):
    dataset = np.array([])

    for directory, substrings, not_substrings, instrument in instruments:
        dataset = concatenate(
            dataset, 
            generate_instrument_dataset(
                directory, 
                substrings, 
                not_substrings, 
                instrument
            )
        )

	# Opcional
	# T = sklearn.decomposition.MiniBatchDictionaryLearning(n_components=1)
	# scomps, sacts = librosa.decompose.decompose(dataset, transformer=T, sort=True)    

    # Generamos la descomposicion de Non-negative matrix
    # dataset = Componentes * Activaciones
    comps, acts = librosa.decompose.decompose(dataset, n_components=len(instruments))
    
    # Calculamos la inversa de Moore-Penrose para sacar la Activacion de los samples de prueba
    # Asi queda dataset * Componentes^(-1) = Activaviones
    comps_inv = linalg.pinv(comps)
    
    print("shape de dataset")
    print(dataset.shape)
    print("shape de W")
    print(comps.shape)
    print(comps_inv.shape)
    print(acts.shape)
    

    return np.array(comps_inv), np.array(acts)

    # [[7.82712577e-03 1.62039602e+02 8.89513943e+01 5.19766760e-03]] - Violin