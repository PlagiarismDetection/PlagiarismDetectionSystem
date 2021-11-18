from pds.database.document import Document
from pds.database.connection import Connection
from pds.candidate_retrieval.pre_processing import WordPreprocessing, NonPreProcessing
from pds.reader.input import readInputs
from pds.candidate_retrieval.candidate import CandidateList
from pds.candidate_retrieval.similarity_metric import SimilarityMetric

database = Connection('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000', 'Documents').getDatabase()

input_vie = readInputs('inputs')
input_vie_pp = WordPreprocessing.VieFilesProcessing(input_vie)
input_vie_none_pp = NonPreProcessing.VieFilesProcessing(input_vie)

collection_vie = Document.getCollection(database, 'vie')
source_vie_pp = WordPreprocessing.VieCollectionProcessing(collection_vie)
collection_vie = Document.getCollection(database, 'vie')
source_vie_none_pp = NonPreProcessing.VieCollectionProcessing(collection_vie)

for input_pp in input_vie_pp:
    SM_list = list(map(lambda source_pp: SimilarityMetric.n_gram_matching(
        input_pp, source_pp, 3, SimilarityMetric.Jaccard_1()), source_vie_pp))
    collection = Document.getCollection(database, 'vie')
    candidate_list = CandidateList(SM_list, collection).get_k_top_similarity(3)
    print(list(map(lambda x: x.getTitle(), candidate_list)))
    print(list(map(lambda x: x.getSM(), candidate_list)))
