VIOLIN   = ("../audios/violin/retocadas_MIS", [], ["trill"], "violin")
FLAUTA   = ("../audios/flauta/retocadas_MIS", [], ["trill"], "flauta")
GUITARRA = ("../audios/guitar/retocadas", [], ["trill"], "guitarra")

VIOLIN_TEST   = (4, "../audios/violin/retocadas_MIS/test", [], [], "violin")
FLAUTA_TEST   = (4, "../audios/flauta/retocadas_MIS/test", [], [], "flauta")
TROMBON_TEST  = (4, "../audios/trombon/retocadas_MIS/test", [], [], "trombon")
GUITARRA_TEST = (4, "../audios/guitar/retocadas/test", [], [], "guitarra")

# Generamos el modelo para predecir
# Generamos la data de test
VIOLIN_TEST   = (4, "../audios/violin/retocadas_MIS/test", [], [], "violin")
FLAUTA_TEST   = (4, "../audios/flauta/retocadas_MIS/test", [], [], "flauta")
TROMBON_TEST  = (4, "../audios/trombon/retocadas_MIS/test", [], [], "trombon")
TROMPETA_TEST = (4, "../audios/trompeta/retocadas_MIS/test", [], [], "trompeta")
GUITARRA_TEST = (4, "../audios/guitar/retocadas/test", [], [], "guitarra")
CLASH_SYMBALS_TEST = (4, "../audios/cymbals/retocadas_MIS/test", [], [], "clash_symbals")

instruments_test = [VIOLIN_TEST, FLAUTA_TEST, TROMBON_TEST, GUITARRA_TEST, CLASH_SYMBALS_TEST, TROMPETA_TEST]

# Generamos el modelo para predecir
instruments = [VIOLIN, FLAUTA, TROMBON, GUITARRA, CLASH_SYMBALS, TROMPETA]
W_inv, H, labels = generate_dataset(instruments=instruments)

# Probamos predecir
instruments_test = [VIOLIN_TEST, FLAUTA_TEST, TROMBON_TEST, GUITARRA_TEST, CLASH_SYMBALS_TEST, TROMPETA_TEST]
dataset = (W_inv, H, labels)

for k, test_path, substring, not_substring, instrument in instruments_test:
    rates = calculateHits(dataset, k, test_path, substring, not_substring, instrument)
    print(str(instrument) + " | hit_rate: " + str(calculateHitRate(rates)))