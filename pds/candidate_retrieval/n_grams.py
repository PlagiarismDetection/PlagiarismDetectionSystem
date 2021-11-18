from abc import ABC
from nltk import ngrams


class NGrams(ABC):
    @staticmethod
    def makeNgrams(token_list, n):
        return ngrams(token_list, n)

    @classmethod
    def makeNgramString(cls, token_list, n):
        ngram_gen = cls.makeNgrams(token_list, n)
        return [' '.join(grams) for grams in ngram_gen]
