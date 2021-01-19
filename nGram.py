def nGramSet(word, size):
    _set = []
    if word.__len__() < size:
        for i in range(size-word.__len__()):
            word+='\0'

    for i in range(word.__len__() - size + 1):
        ngram = ''
        for j in range(size):
            ngram += (word[i + j]);
        _set.append(ngram)
    return _set


def jaccard_coeff(set1, set2):
    union = list(set(set1) | set(set2))
    intersection = list(set(set1) & set(set2))
    return intersection.__len__()/union.__len__()
