import re

from nltk import word_tokenize, sent_tokenize
# module for stop words that come with NLTK
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer         # module for stemming
from nltk.stem import WordNetLemmatizer     # module for lemmatization

# Get punctuations sring from NLTK
punctuations = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~…“”–"""


class EngPreprocessing():
    def __init__(self):
        pass

    @classmethod
    def preprocess2sent(cls, input):
        text = cls.replace_num(input)
        text = cls.lowercasing(text)
        sent_list = sent_tokenize(text)

        return sent_list

    @classmethod
    def preprocess2word(cls, input):
        text = cls.replace_num(input)
        text = cls.lowercasing(text)
        tokens = word_tokenize(text)
        tokens_clean = cls.rm_stopword_punct(tokens)
        # tokens_stem = cls.stemming(tokens_clean)

        return tokens_clean

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
    def lowercasing(cls, text):
        text1 = text
        return text1.lower()

    @staticmethod
    def tokenization(text):
        return word_tokenize(text)

    @classmethod
    def rm_stopword_punct(cls, tokens):
        stopwords_english = stopwords.words('english')
        tokens_clean = []

        for word in tokens:                         # Go through every word in your tokens list
            if (word not in stopwords_english and   # remove stopwords
                    word not in punctuations):      # remove punctuation
                tokens_clean.append(word)
        return tokens_clean

    @classmethod
    def stemming(cls, tokens):
        # Instantiate stemming class
        stemmer = PorterStemmer()

        # Create an empty list to store the stems
        tokens_stem = []

        for word in tokens:
            stem_word = stemmer.stem(word)  # stemming word
            tokens_stem.append(stem_word)   # append to the list
        return tokens_stem

    @classmethod
    def lemmatize(cls, tokens):
        # Instantiate stemming class
        lemmatizer = WordNetLemmatizer()

        # Create an empty list to store the stems
        tokens_lemma = []

        for word in tokens:
            lemma_word = lemmatizer.lemmatize(word)  # stemming word
            tokens_lemma.append(lemma_word)         # append to the list
        return tokens_lemma
