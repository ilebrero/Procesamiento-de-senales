import sklearn.decomposition
import librosa

from os import listdir, mkdir
from os.path import isfile, join, splitext, getsize

from numpy import linalg

def count(files):
    count = dict()

    for file in files:
        file_size = file[1]

        if file_size in count.keys():
            count[file_size] = count[file_size] + 1
        else:
            count[file_size] = 1

    return count

def first_elements(lst):
    check = lst[0][1]
    elems = []

    for elem in lst:
        if elem[1] == check:
            elems.append(elem[0])
        else:
            break

    return elems

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

    # filepaths = []

    # for i in range(len(all_paths)):
    #     filepaths.append(
    #     	(
    #     		all_paths[i], 
    #     		getsize(
    #     			join(
    #     				directory, 
    #     				all_paths[i]
    #     				)
    #     			)
    #     		)
    #     	)

    # counts = count(filepaths)
    # filepaths = sorted(filepaths, key=lambda x: counts[x[1]], reverse=True)

    # Me quedo con los que mas aparecen
    # return first_elements(filepaths)
    return all_paths

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

def get_audio_features(file_path):
    y, sr = librosa.load(file_path)
    return generate_audio_features(y, sr)


def generate_stacked_new_row(a, b):
    if a.size == 0: return b # Caso especial si a no tiene elems todavia
    return np.vstack( (a, b) )

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

def concatenate(a, b):
    if a.size == 0: return b
    return np.concatenate((a, b))

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
    # Nota: transponemos el dataset para tener los features como filas (ver paper)
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