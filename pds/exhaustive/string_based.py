from abc import ABC
from pds.candidate_retrieval.n_grams import NGrams


class StringBasedTechnique(ABC):
    @staticmethod
    def __rabin_karp_with_hashing(pattern, text, q):
        M = len(pattern)
        N = len(text)
        if M > N: return False
        i = 0
        j = 0
        p = 0
        t = 0
        h = 1
        d = 256

        # The value of h would be "pow(d, M-1)%q"
        for i in range(M-1):
            h = (h*d) % q
            # Calculate the hash value of pattern and first window
            # of text
        for i in range(M):
            p = (d*p + ord(pattern[i])) % q
            t = (d*t + ord(text[i])) % q
            # Slide the pattern over text one by one
        for i in range(N-M+1):
            if p == t:
                # Check for characters one by one
                for j in range(M):
                    if text[i+j] != pattern[j]:
                        break
                    else:
                        j += 1
                if j == M:
                    return True

            if i < N-M:
                t = (d*(t-ord(text[i])*h) + ord(text[i+M])) % q
                if t < 0:
                    t = t+q
        return False

    @classmethod
    def n_gram_matching(cls, input_sent_list, candidate_sent_list, grams_num, hash_prime):
        result = []
        for input_sent in input_sent_list:
            input_grams = NGrams.makeNgramString(
                input_sent.getWords(), grams_num)
            for gram in input_grams:
                similar = []
                for candidate_sent in candidate_sent_list:
                    sent = candidate_sent.getSentence()
                    if cls.__rabin_karp_with_hashing(gram, sent, hash_prime):
                        similar.append(sent)
                if len(similar) > 0:
                    result.append((input_sent, similar))
                    break
        return result
