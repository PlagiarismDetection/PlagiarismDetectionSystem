from abc import ABC


class FileObj(ABC):
    def __init__(self):
        pass

    def getType(self):
        pass

    def getTitle(self):
        pass

    def getAuthor(self):
        pass

    def getDate(self):
        pass

    def getContent(self):
        pass


class Reader(ABC):
    def __init__(self):
        pass
