# library for regular expression operations
import re
# library for standardlize VNM, download from https://gist.github.com/nguyenvanhieuvn/72ccf3ddf7d179b281fdae6c0b84942b
from PreProcessing.nlp_utils import *
# library for VNM word tokenization
from underthesea import word_tokenize, sent_tokenize

# Import the Vietnamese stopwords file, download from: https://github.com/stopwords/vietnamese-stopwords
f = open('PreProcessing/vietnamese-stopwords.txt', 'r')
vnm_stopwords = f.read().splitlines()
f.close()

# Get punctuations sring from NLTK
punctuations = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~…“”–"""


class VnmPreprocessing():
    def __init__(self):
        pass

    @classmethod
    def preprocess2sent(cls, input):
        text = cls.replace_num(input)
        text = cls.standardize_unicode(text)
        text = cls.standardize_marks(text)
        text = cls.lowercasing(text)

        sent_list = sent_tokenize(text)

        return sent_list

    @classmethod
    def preprocess2word(cls, input):
        text = cls.replace_num(input)
        text = cls.standardize_unicode(text)
        text = cls.standardize_marks(text)

        tokens = word_tokenize(text)
        tokens_clean = cls.lower_rm_stopword_punct(tokens)

        return tokens_clean

    @staticmethod
    def tokenization(text):
        return word_tokenize(text)

    @classmethod
    def replace_num(cls, text):
        newtext = text

        # remove date time ?
        newtext = re.sub(r'\d+[/-]\d+([/-]\d+)*', ' date', newtext)
        newtext = re.sub(r'\d+[:]\d+([:]\d+)*', ' time', newtext)

        # remove currency ?
        # newtext = re.sub(r'\d+([.,]\d+)*$', ' dollar', newtext)
        # newtext = re.sub(r'$\d+([.,]\d+)*', ' dollar', newtext)

        # remove simple int number, float number may be following space or "(" like "(12.122.122)"
        newtext = re.sub(r'-?\d+([.,]\d+)*', ' num', newtext)
        return newtext

    @classmethod
    def standardize_unicode(cls, text):
        std_uni_text = convert_unicode(text)
        return std_uni_text

    @classmethod
    def standardize_marks(cls, text):
        std_marks_text = chuan_hoa_dau_cau_tieng_viet(text)
        return std_marks_text

    @classmethod
    def lowercasing(cls, text):
        text1 = text
        return text1.lower()

    @classmethod
    def lower_rm_stopword_punct(cls, tokens):
        tokens_clean = []

        for word in tokens:                         # Go through every word in your tokens list
            word = word.lower()                     # Lowercasing
            if (word not in vnm_stopwords and       # remove stopwords
                    word not in punctuations):      # remove punctuation
                tokens_clean.append(word)
        return tokens_clean
