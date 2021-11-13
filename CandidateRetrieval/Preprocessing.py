from PreProcessing.VnmPreprocessing import VnmPreprocessing
from PreProcessing.EngPreprocessing import EngPreprocessing
from abc import ABC


class Preprocessing(ABC):
    @staticmethod
    def VieCollectionProcessing(collection):
        pass

    @staticmethod
    def EngCollectionProcessing(collection):
        pass


class WordPreprocessing(Preprocessing):
    @staticmethod
    def VieCollectionProcessing(collection):
        return list(map(lambda item: VnmPreprocessing.preprocess2word(item['Content']), collection))

    @staticmethod
    def EngCollectionProcessing(collection):
        return list(map(lambda item: EngPreprocessing.preprocess2word(item['Content']), collection))

    @staticmethod
    def VieFilesProcessing(files):
        return list(map(lambda item: VnmPreprocessing.preprocess2word(item.getContent()), files))

    @staticmethod
    def EngFilesProcessing(files):
        return list(map(lambda item: EngPreprocessing.preprocess2word(item.getContent()), files))


class NonPreProcessing(Preprocessing):
    @staticmethod
    def VieCollectionProcessing(collection):
        return list(map(lambda item: VnmPreprocessing.tokenization(item['Content']), collection))

    @staticmethod
    def EngCollectionProcessing(collection):
        return list(map(lambda item: EngPreprocessing.tokenization(item['Content']), collection))

    @staticmethod
    def VieFilesProcessing(files):
        return list(map(lambda item: VnmPreprocessing.tokenization(item.getContent()), files))

    @staticmethod
    def EngFilesProcessing(files):
        return list(map(lambda item: EngPreprocessing.tokenization(item.getContent()), files))
