from pds.database.document import Document
from pds.candidate_retrieval.pre_processing import WordPreprocessing
from pds.pre_processing.vnm_preprocessing import VnmPreprocessing
from pds.reader.input import readInput
from pds.candidate_retrieval.candidate import CandidateList
from pds.candidate_retrieval.similarity_metric import SimilarityMetric
from pds.exhaustive.sentence import EngSentence, VieSentence
from pds.exhaustive.string_based import StringBasedTechnique
from pds.exhaustive.result import Evidence, Result
import re


def remove_dumb_sent(text):
    cleanStr = re.sub('[.-:]+', '', text)
    return cleanStr


def vie_offline_string_based_with_rabinkarp(database, collection, input_path, candidate_num, metric, ngrams_num, hash_prime):
    input_vie = readInput(input_path)

    if input_vie:
        # Step 1: Preprocessing
        input_vie_pp = WordPreprocessing.VieFilesProcessing(input_vie)

        collection_vie = Document.getCollection(database, collection)
        source_vie_pp = list(
            map(lambda item: item['Content-word'], collection_vie))

        print('Preprocessing done!')
        # Step 2: Candidate retrieval
        SM_list = list(map(lambda source_pp: SimilarityMetric.n_gram_matching(
            input_vie_pp, source_pp, 3, metric), source_vie_pp))

        col = Document.getCollection(database, collection)
        candidate_list = CandidateList(
            SM_list, col).get_k_top_similarity(candidate_num)

        print('Candidate Retrieval done!')
        # Step 3: Exhaustive Comparison
        result = Result(input_vie.getTitle())

        input_sent_list = VnmPreprocessing.sentence_split(
            input_vie.getContent())
        input_sent_list = list(
            map(lambda sent: remove_dumb_sent(sent), input_sent_list))
        input_sent_list = list(
            filter(lambda sent: len(sent) != 0, input_sent_list))
        input_sent_list_with_word = list(
            map(lambda sent: VieSentence(sent), input_sent_list))

    for candidate in candidate_list:
        candidate_sent_list = VnmPreprocessing.sentence_split(
            candidate.getContent())
        candidate_sent_list = list(
            map(lambda sent: remove_dumb_sent(sent), input_sent_list))
        candidate_sent_list = list(
            filter(lambda sent: len(sent) != 0, input_sent_list))
        candidate_sent_list_with_word = list(
            map(lambda sent: VieSentence(sent), candidate_sent_list))
        evidence = Evidence(candidate.getTitle(), StringBasedTechnique.n_gram_matching(
            input_sent_list_with_word, candidate_sent_list_with_word, ngrams_num, hash_prime))
        result.addEvidence(evidence)

    result.print()
