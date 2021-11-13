from collections import defaultdict
from abc import ABC
from CandidateRetrieval.Ngrams import NGrams
from nltk.corpus import wordnet as wn
import math


class SimilarityMetric(ABC):
    @staticmethod
    def __n_gram_matching_SM_with_Jaccard(input_grams, source_grams):
        lst = [value for value in input_grams if value in source_grams]
        return len(lst)/(len(input_grams)+len(source_grams)-len(lst))

    @staticmethod
    def __n_gram_matching_SM_with_Jaccard_variant_1(input_grams, source_grams):
        lst = [value for value in input_grams if value in source_grams]
        return len(lst)/len(input_grams)

    @staticmethod
    def __n_gram_matching_SM_with_Jaccard_variant_2(input_grams, source_grams):
        lst = [value for value in input_grams if value in source_grams]
        return len(lst)/min(len(input_grams), len(source_grams))

    @staticmethod
    def __training_bigrams(source_tokens):
        model = defaultdict(lambda: defaultdict(lambda: 0))

        for w1, w2 in NGrams.makeNgrams(source_tokens, 2):
            model[w1][w2] += 1

        for w1 in model:
            total_count = float(sum(model[w1].values()))
            for w2 in model[w1]:
                model[w1][w2] /= total_count
        return model

    @staticmethod
    def n_gram_matching(input_tokens, source_tokens, n, metric):
        input_grams = NGrams.makeNgramString(input_tokens, n)
        source_grams = NGrams.makeNgramString(source_tokens, n)
        return metric(input_grams, source_grams)

    @staticmethod
    def lcs(input_tokens, source_tokens):
        m = len(input_tokens)
        n = len(source_tokens)
        L = [[None]*(n + 1) for i in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif input_tokens[i-1] == source_tokens[j-1]:
                    L[i][j] = L[i-1][j-1]+1
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])
        return math.log2(1 + L[m][n]/n)

    @staticmethod
    def lexical_generalization(input_tokens, source_tokens):
        input_synset = list(map(lambda word: wn.synsets(word), input_tokens))
        source_synset = list(map(lambda word: wn.synsets(word), source_tokens))
        intersection = 0
        for i in input_synset:
            for s in source_synset:
                lst = [value for value in i if value in s]
                if len(lst) > 0:
                    intersection += 1
        return intersection / (len(input_tokens)+len(source_tokens)-intersection)

    @classmethod
    def language_model(cls, input_tokens, source_tokens):
        input_grams = NGrams.makeNgrams(input_tokens, 2)
        model = cls.__training_bigrams(source_tokens)
        P_input = 1
        for w1, w2 in input_grams:
            if model[w1][w2] != 0:
                P_input *= model[w1][w2]
            else:
                P_input *= 0.0001
        return P_input

    @classmethod
    def Jaccard(cls):
        return cls.__n_gram_matching_SM_with_Jaccard

    @classmethod
    def Jaccard_1(cls):
        return cls.__n_gram_matching_SM_with_Jaccard_variant_1

    @classmethod
    def Jaccard_2(cls):
        return cls.__n_gram_matching_SM_with_Jaccard_variant_2
