from pds.offline_string_based import vie_offline_string_based_with_rabinkarp
from pds.database.connection import Connection
from pds.candidate_retrieval.similarity_metric import SimilarityMetric

database = Connection(
    'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000', 'Documents').getDatabase()

vie_offline_string_based_with_rabinkarp(
    database, 'vie', 'Inputs', 3, SimilarityMetric.Jaccard_1(), 5, 101)
