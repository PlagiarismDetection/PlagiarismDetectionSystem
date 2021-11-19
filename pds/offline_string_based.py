from pds.database.document import Document
from pds.database.connection import Connection
from pds.candidate_retrieval.pre_processing import WordPreprocessing
from pds.exhaustive.result import SimilarPair
from pds.pre_processing.vnm_preprocessing import VnmPreprocessing
from pds.reader.input import readInput
from pds.candidate_retrieval.candidate import CandidateList
from pds.candidate_retrieval.similarity_metric import SimilarityMetric
from pds.exhaustive.sentence import EngSentence, VieSentence
from pds.exhaustive.string_based import StringBasedTechnique
from pds.exhaustive.result import Evidence, Result


def vie_cr_offline_string_based_with_rabinkarp(database, collection, input_path, candidate_num, metric, ngrams_num, hash_prime):
    input_vie = readInput(input_path)

    if len(input_vie) == 0:
        return 'Input folder must contain a file'

    # Step 1: Preprocessing
    input_vie_pp = WordPreprocessing.VieFilesProcessing(input_vie)

    collection_vie = Document.getCollection(database, collection)
    source_vie_pp = list(
        map(lambda item: item['Content-word'], collection_vie))

    # Step 2: Candidate retrieval
    SM_list = list(map(lambda source_pp: SimilarityMetric.n_gram_matching(
        input_vie_pp, source_pp, 3, metric), source_vie_pp))

    collection = Document.getCollection(database, collection)
    candidate_list = CandidateList(
        SM_list, collection).get_k_top_similarity(candidate_num)

    # Step 3: Exhaustive Comparison
    result = Result(input_vie.getTitle())

    candidate_list_full = list(map(lambda candidate: Document.getDocument(
        database, collection, {'Title': candidate.getTitle()}), candidate_list))
    input_sent_list = VnmPreprocessing.sentence_split(
        input_vie.getContent())
    input_sent_list_with_word = list(
        map(lambda sent: VieSentence(sent), input_sent_list))

    for candidate in candidate_list_full:
        candidate_sent_list = VnmPreprocessing.sentence_split(
            candidate['Content'])
        candidate_sent_list_with_word = list(
            map(lambda sent: VieSentence(sent), candidate_sent_list))
        evidence = Evidence(candidate['Title'], StringBasedTechnique.n_gram_matching(
            input_sent_list_with_word, candidate_sent_list_with_word, ngrams_num, hash_prime))
        result.addEvidence(evidence)

    result.print()


database = Connection(
    'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000', 'Documents').getDatabase()

vie_cr_offline_string_based_with_rabinkarp(
    database, 'vie', 'Inputs', 3, SimilarityMetric.Jaccard_1(), 5, 101)
