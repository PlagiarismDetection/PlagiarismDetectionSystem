from .EngPreprocessing import *
from .VnmPreprocessing import *

from nltk import download

# download the English stopwords from NLTK
download('stopwords')
# download the pre-trained Punkt tokenizer for English, using for PorterStemmer module
download('punkt')
# download wornet for English, using for WordNetLemmatizer module
download('wordnet')
