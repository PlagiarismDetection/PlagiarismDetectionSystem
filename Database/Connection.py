from pymongo import MongoClient
from abc import ABC


class Connection(ABC):
    def __init__(self, CONNECTION_STRING, dbname) -> None:
        super().__init__()
        self.dbname = self.__connect(CONNECTION_STRING, dbname)

    @staticmethod
    def __connect(CONNECTION_STRING, dbname):
        client = MongoClient(CONNECTION_STRING)
        return client[dbname]

    def getDatabase(self):
        return self.dbname
