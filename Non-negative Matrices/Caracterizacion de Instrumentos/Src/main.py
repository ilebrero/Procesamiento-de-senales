from sklearn.metrics import confusion_matrix

VIOLIN   = ("../audios/violin/retocadas_MIS", [], ["trill"], "violin")
FLAUTA   = ("../audios/flauta/retocadas_MIS", [], ["trill"], "flauta")
GUITARRA = ("../audios/guitar/retocadas", [], ["trill"], "guitarra")

VIOLIN_TEST   = (4, "../audios/violin/retocadas_MIS/test", [], [], "violin")
FLAUTA_TEST   = (4, "../audios/flauta/retocadas_MIS/test", [], [], "flauta")
TROMBON_TEST  = (4, "../audios/trombon/retocadas_MIS/test", [], [], "trombon")
TROMPETA_TEST = (4, "../audios/trompeta/retocadas_MIS/test", [], [], "trompeta")
GUITARRA_TEST = (4, "../audios/guitar/retocadas/test", [], [], "guitarra")
CLASH_SYMBALS_TEST = (4, "../audios/cymbals/retocadas_MIS/test", [], [], "clash_symbals")

# Generamos el modelo para predecir y los datos de tests
instruments 	 = [VIOLIN, FLAUTA, TROMBON, GUITARRA, CLASH_SYMBALS, TROMPETA]
instruments_test = [VIOLIN_TEST, FLAUTA_TEST, TROMBON_TEST, GUITARRA_TEST, CLASH_SYMBALS_TEST, TROMPETA_TEST]

for cant_componentes in range(6, 7):
    print("pruebo con cantidad de componentes: " + str(cant_componentes))
    
    # Entrenamos el modelo
    W_inv, H, labels = generate_dataset(instruments=instruments, components=cant_componentes)

    expected_values  = []
    predicted_values = []

    for k, test_path, substring, not_substring, instrument in instruments_test:
        
        # Calculamos la prediccion
        success, fails, predicted_labels = calculateHits(dataset, k, test_path, substring, not_substring, instrument)
        hit_rate = calculateHitRate((success, fails, predicted_labels))

        # Appendeamos a los hit rates historicos
        overall_hit_rates[instrument].append(hit_rate)

        # Agregamos a los valores historicos predichos
        predicted_values = predicted_values + predicted_labels    

        # Agregamos el label actual para matchear a los predichos
        for i in predicted_labels:
            expected_values.append(instrument)

        print(str(instrument) + " | hit_rate: " + str(hit_rate))
        
    conf_matrix = confusion_matrix(
        expected_values, 
        predicted_values,
        labels=["violin", "flauta", "trombon", "guitarra", "clash_symbals", "trompeta"]
    ) 
        
    # Calculamos la matriz de confusion actual
    confusion_matrices.append(conf_matrix)

    print("Matriz de Confusion")
    print(conf_matrix)
    print("\n ------------------------------------ \n")