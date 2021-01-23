import sys
import threading
import time
import editDistance
import nGram
import random
from memory_usage_thread import MemoryUsageThread

lexica = [
    "paroleitaliane/paroleitaliane/1000_parole_italiane_comuni.txt",
    "paroleitaliane/paroleitaliane/400_parole_composte.txt",
    "paroleitaliane/paroleitaliane/9000_nomi_propri.txt",
    "paroleitaliane/paroleitaliane/lista_badwords.txt",
    "paroleitaliane/paroleitaliane/110000_parole_italiane_con_nomi_propri.txt",
    "paroleitaliane/paroleitaliane/60000_parole_italiane.txt",
    "paroleitaliane/paroleitaliane/95000_parole_italiane_con_nomi_propri.txt",
    "paroleitaliane/paroleitaliane/lista_cognomi.txt",
    "paroleitaliane/paroleitaliane/280000_parole_italiane.txt",
    "paroleitaliane/paroleitaliane/660000_parole_italiane.txt",
    "paroleitaliane/paroleitaliane/lista_38000_cognomi.txt",
    "paroleitaliane/paroleitaliane/parole_uniche.txt"
]

lessico_L = []

ngram_test_results = []
edit_distance_test_results = []


def extractWordsFromLexica(amount, lexicon):
    return random.choices(lexicon, k=amount)


# swappa word.__len__()/2 caratteri
def shuffleWord(word):
    tmpword = list(word)
    _range = list(range(0, word.__len__()))
    indexes = random.choices(_range, k=round(word.__len__() / 2))
    for i in range(0, indexes.__len__(), 2):
        tmp = tmpword[i]
        tmpword[i] = tmpword[i + 1]
        tmpword[i + 1] = tmp

    return "".join(tmpword)


def generateLexicon(_lexica):
    print("Generazione dell'intero vocabolario...")
    lexicon = []

    # generazione intero vocabolario
    for _dict in _lexica:
        print(_dict)
        buf = []
        file = open(_dict, 'r')
        buf = file.readlines(1)
        while buf:
            line = buf[0]

            # cancellazione carattere '\n'
            if line[-1:] == '\n':
                line = line[0:-1]

            lexicon.append(line)
            buf = file.readlines(1)

        file.close()

    return lexicon


def test_common_setup(test_function, maxpow):
    # generazione vettore delle grandezze dei vari insiemi di query
    grandezze_array = list(range(0, maxpow))
    for i in range(grandezze_array.__len__()):
        grandezze_array[i] = pow(2, grandezze_array[i])

    # estrazione di alcune parole
    for size in grandezze_array:
        print("Query di", size, "parole \nEstrazione...")
        query_Q = extractWordsFromLexica(size, lessico_L)

        # distorsione del 40% delle parole estratte, per simulare le parole assenti dall'insieme
        indexes = random.sample(range(0, query_Q.__len__()), k=round(query_Q.__len__() * 0.4))
        for index in indexes:
            query_Q[index] = shuffleWord(query_Q[index])

        # confronti
        print("Inizio...")
        start = time.time()
        test_function(query_Q)
        print("Eseguita in", time.time() - start, "secondi")
    return


def edit_distance_test_function(query_Q):
    for parola in query_Q:
        for vocabolo in lessico_L:
            distance = editDistance.editDistance(parola, vocabolo)
            if distance == 0:
                edit_distance_test_results.append((parola, vocabolo))
    return


def edit_distance_test(maxpow=2):
    print("Inizio test Edit-Distance")

    test_common_setup(lambda queryQ: edit_distance_test_function(queryQ), maxpow)
    return


def ngram_test_function(query_Q, ngram_size):
    for parola in query_Q:
        ngram_set1 = nGram.nGramSet(parola, ngram_size)

        for vocabolo in lessico_L:
            ngram_set2 = nGram.nGramSet(vocabolo, ngram_size)
            jaccard = nGram.jaccard_coeff(ngram_set1, ngram_set2)

            if jaccard > 0.8:
                ngram_test_results.append((vocabolo, jaccard))
    return


def ngram_test(ngram_size,maxpow=2):
    print("Inizio test n-grammi")

    test_common_setup(lambda queryQ: ngram_test_function(queryQ, ngram_size), maxpow)
    return


def main():
    print(sys.version)

    # inizializzo il thread per misurare l'utilizzo di memoria
    mem_thread = MemoryUsageThread()
    mem_usg_thread = threading.Thread(target=mem_thread.run, daemon=True)
    mem_usg_thread.start()
    #

    # generazione del lessico
    start_time = time.time()
    global lessico_L
    lessico_L = generateLexicon(lexica)
    print("Generazione completata. Tempo impiegato:", time.time() - start_time, "secondi")
    #

    # INIZIO DEI TEST
    if "--no-ngram" not in sys.argv:
        start_time = time.time()
        ngram_test(3)
        print("Test completato. Tempo impiegato:", time.time() - start_time, "secondi")

    if "--no-edist" not in sys.argv:
        start_time = time.time()
        edit_distance_test()
        print("Test completato. Tempo impiegato:", time.time() - start_time, "secondi")
    # FINE DEI TEST

    print(ngram_test_results)

    global mem_usg_thr_has_to_stop
    mem_usg_thr_has_to_stop = True

    return


if __name__ == '__main__':
    main()
