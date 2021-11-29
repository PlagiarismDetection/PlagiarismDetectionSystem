from abc import ABC
from pds.candidate_retrieval.n_grams import NGrams
from pds.candidate_retrieval.similarity_metric import SimilarityMetric
import numpy as np


class StringBasedTechnique(ABC):
    # @staticmethod
    # def __rabin_karp_with_hashing(pattern, text, q):
    #     M = len(pattern)
    #     N = len(text)
    #     if M > N:
    #         return False
    #     i = 0
    #     j = 0
    #     p = 0
    #     t = 0
    #     h = 1
    #     d = 256

    #     # The value of h would be "pow(d, M-1)%q"
    #     for i in range(M-1):
    #         h = (h*d) % q
    #         # Calculate the hash value of pattern and first window
    #         # of text
    #     for i in range(M):
    #         p = (d*p + ord(pattern[i])) % q
    #         t = (d*t + ord(text[i])) % q
    #         # Slide the pattern over text one by one
    #     for i in range(N-M+1):
    #         if p == t:
    #             # Check for characters one by one
    #             for j in range(M):
    #                 if text[i+j] != pattern[j]:
    #                     break
    #                 else:
    #                     j += 1
    #             if j == M:
    #                 return True

    #         if i < N-M:
    #             t = (d*(t-ord(text[i])*h) + ord(text[i+M])) % q
    #             if t < 0:
    #                 t = t+q
    #     return False

    @staticmethod
    def n_gram_matching(input_sent_list, candidate_sent_list, grams_num):
        input_grams_list = list(
            map(lambda input_sent: input_sent.getWord(), input_sent_list))
        candidate_grams_list = list(
            map(lambda candidate_sent: candidate_sent.getWord(), candidate_sent_list))
        evidence_SM = np.array([])

        for input_gram in input_grams_list:
            for candidate_gram in candidate_grams_list:
                evidence_SM = np.append(evidence_SM, SimilarityMetric.n_gram_matching(
                    input_gram, candidate_gram, grams_num, SimilarityMetric.Jaccard_2()))
        return np.reshape(evidence_SM, (len(input_sent_list), len(candidate_sent_list)))
