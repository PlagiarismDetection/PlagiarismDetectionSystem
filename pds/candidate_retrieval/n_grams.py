from abc import ABC
from nltk import ngrams


class NGrams(ABC):
    @staticmethod
    def makeNgrams(token_list, n):
        return ngrams(token_list, n, pad_left=False, pad_right=True, right_pad_symbol=' ')

    @classmethod
    def makeNgramString(cls, token_list, n):
        if len(token_list) >= n:
            ngram_gen = cls.makeNgrams(token_list, n)
            return [' '.join(grams) for grams in ngram_gen]
        return [' '.join(token_list)]
