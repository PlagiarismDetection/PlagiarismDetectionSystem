from abc import ABC
from pds.pre_processing.vnm_preprocessing import VnmPreprocessing
from pds.pre_processing.eng_preprocessing import EngPreprocessing


class VieSentence(ABC):
    def __init__(self, sentence_text):
        super().__init__()
        self.words = VnmPreprocessing.tokenization(sentence_text)
        self.sentence = sentence_text

    def getWords(self):
        return self.words

    def getSentence(self):
        return self.sentence


class EngSentence(ABC):
    def __init__(self, sentence_text):
        super().__init__()
        self.words = EngPreprocessing.tokenization(sentence_text)
        self.sentence = sentence_text

    def getWords(self):
        return self.words

    def getSentence(self):
        return self.sentence
