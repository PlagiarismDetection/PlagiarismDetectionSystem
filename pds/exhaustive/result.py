from abc import ABC

from pds.candidate_retrieval.candidate import Candidate


class Evidence(ABC):
    def __init__(self, candidate, evidence_list):
        super().__init__()
        self.candidate = candidate
        self.evidence_list = evidence_list

    def getCandidate(self):
        return self.candidate

    def getEvidenceList(self):
        return self.evidence_list


class Result(ABC):
    def __init__(self, input_title):
        super().__init__()
        self.input_title = input_title
        self.evidence_list = []

    def getInputTitle(self):
        return self.input_title

    def getEvidenceList(self):
        return self.evidence_list

    def addEvidence(self, evidence):
        if evidence == []:
            return
        self.evidence_list.append(evidence)

    def print(self):
        print('Input title: ' + self.getInputTitle())
        print('Plagiarism source texts suspicious:')
        for evidence in self.getEvidenceList():
            candidate = evidence.getCandidate()
            evidence_list = evidence.getEvidenceList()
            print('    Title: ' + candidate.getTitle() +
                  ' with similarity score: ' + candidate.getSM())
            print('    Similar sentences:')
            for e in evidence_list:
                print('        Your text: ' +
                      e[0] + ' vs. Source text: ' + e[1])
