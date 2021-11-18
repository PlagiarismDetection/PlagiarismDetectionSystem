from abc import ABC
import operator


class Candidate(ABC):
    def __init__(self, SM, document):
        super().__init__()
        self.title = document['Title']
        self.author = document['Author']
        self.created_time = document['Created-time']
        self.sm = SM

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getCreatedTime(self):
        return self.created_time

    def getSM(self):
        return self.sm


class CandidateList(ABC):
    def __init__(self, SM_List, collection):
        super().__init__()
        self.candidate_list = self.__getCandidateList(SM_List, collection)

    def get_candidate_list(self):
        return self.candidate_list

    def get_k_top_similarity(self, k):
        candidate_list = self.get_candidate_list()
        candidate_list_sorted = sorted(
            candidate_list, key=operator.attrgetter('sm'), reverse=True)
        return candidate_list_sorted[:k]

    @staticmethod
    def __getCandidateList(SM_List, collection):
        index = 0
        candidate_list = []
        for document in collection:
            candidate_list.append(Candidate(SM_List[index], document))
            index += 1
        return candidate_list
