import re
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from PreProcessing import VnmPreprocessing, EngPreprocessing
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk import ngrams

class CROnline():
    def __init__(self):
        pass

    @staticmethod
    def split_to_paras(data):
        punctuations = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~…“”–"""
        temp1 = re.sub(r'\n\n+', '@@@', data)
        temp2 = re.sub(r'\n', ' ', temp1)
        data_text = re.sub('@@@', '\n', temp2)
        data_list = data_text.split('\n')

        para_list = []
        for par in data_list:
            if len(par) > 200:
                if not par[0].isdigit() and not par[0] in punctuations:
                    if not re.match(r"[.−_]{3,}", par):
                        para_list.append(par)
        return para_list

    @classmethod
    def chunking(cls, data):
        # Split data text to get important paragraph
        para_list = cls.split_to_paras(data)

        # Chunking each paragraph to chunk of 1 - 3 sentences.
        # Use Preprocessing to sent to split each paragraph to list of sent.
        # Chunk has n sentences, if n/3 = 1 => last chunk has 4 sents, else chunking to 2 - 3 sentences.
        # Combine all sentences of a chunk to 1 string, filter if chunk has less than 100 character, and add to chunklist.
        chunk_list = []

        for par in para_list:
            # Use Preprocessing to sent to split each paragraph to list of sent.
            sent_list = EngPreprocessing.preprocess2sent(par)

            # Chunking each paragraph to many chunks of 2 - 4 sentences.
            chunks = [sent_list[i: i + 3] for i in range(0, len(sent_list), 3)]

            if len(sent_list) > 3 & len(sent_list) % 3 == 1:
                chunks[-2] += chunks[-1]
                chunks = chunks[:-1]

            # Combine all sentences of a chunk to 1 string
            chunks = [' '.join(c) for c in chunks]
            print(chunks)

            # Filter for chunk > 100 char, and add to chunklist.
            # filter(lambda c: len(c) > 100, chunks)
            chunk_list += [c for c in chunks if len(c) > 100]

        # print(len(chunk_list))
        # print([len(c) for c in chunk_list])
        # print(chunk_list)
        return chunk_list

    @staticmethod
    def preprocess_chunk_list(chunk_list):
        # Preprocessing a chunk to remove stopword and punctuation.
        # Filtering chunk >= 10 word, word >= 4 and not contain special words.
        pp_chunk_list = [EngPreprocessing.preprocess2word(chunk) for chunk in chunk_list]
        pp_chunk_list = [list(filter(lambda w: (len(w) >= 4) & (w not in ['date', 'time', 'http', 'https']) & (
            not w.startswith(r"//")), chunk)) for chunk in pp_chunk_list]
        pp_chunk_list = list(filter(lambda c: (len(c) >= 10), pp_chunk_list))
        return pp_chunk_list

    @staticmethod
    def get_top_tf_idf_words(pp_chunk_list, top_k=20):
        # instantiate the vectorizer object
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')

        # convert documents into a matrix
        chunk_list = [' '.join(c) for c in pp_chunk_list]
        features = tfidf_vectorizer.fit_transform(chunk_list)

        # retrieve the terms found in the corpora
        feature_names = np.array(tfidf_vectorizer.get_feature_names())

        # TF-IDF score matrix
        df_tfidfvect = pd.DataFrame(data=features.toarray(), index=[
                                    i for i in range(len(chunk_list))], columns=feature_names)

        sorted_nzs = np.argsort(features.data)[:-(top_k+1):-1]
        top_list = [feature_names[features.indices[sorted_nzs]]
                    for feature in features]
        return top_list

    @classmethod
    def query_formulate(cls, chunk_list, top_k=20):
        pp_chunk_list = cls.preprocess_chunk_list(chunk_list)
        query1_list = ["+".join(w[:20]) for w in pp_chunk_list]

        top_list = cls.get_top_tf_idf_words(pp_chunk_list, top_k)
        query2_list = ["+".join(top) for top in top_list]

        return query1_list + query2_list

    @staticmethod
    def searchBing(query):
        get_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        s = requests.Session()
        url = 'https://www.bing.com/search?q=' + query + \
            "+filetype%3A&go=Search&qs=ds&form=QBRE"

        page = s.get(url, headers=get_header)
        soup = BeautifulSoup(page.text, "html.parser")

        output = []
        # this line may change in future based on google's web page structure
        for searchWrapper in soup.find_all('li', attrs={'class': 'b_algo'}):
            url = searchWrapper.find('a')["href"]
            title = searchWrapper.find('a').text.strip()

            snippet = searchWrapper.find('p')
            snippet = "" if snippet == None else snippet.text

            res = {'title': title, 'url': url, 'snippet': snippet}
            # print(res)
            output.append(res)

        return output

    @classmethod
    def search_control(cls, query_list):
        result = []
        for query in query_list:
            urls = cls.searchBing(query)
            result += urls

        return result

    @classmethod
    def download_filtering_hybrid(cls, search_results, suspicious_doc_string, language='vi'):
        check_duplicated = cls.check_duplicate_url(search_results)
        if language == 'vi':
            return cls.snippet_based_checking_vi(check_duplicated, suspicious_doc_string)
        elif language == 'en':
            return cls.snippet_based_checking_en(check_duplicated, suspicious_doc_string)

    @staticmethod
    def check_duplicate_url(search_results):
        check_duplicated = []
        url_list = []
        title_list = []

        for search_res in search_results:
            if (search_res['url'] not in url_list) and (search_res['title'] not in title_list):
                check_duplicated.append(search_res)
                url_list.append(search_res['url'])
                title_list.append(search_res['title'])
        return check_duplicated

    @staticmethod
    def snippet_based_checking_en(search_results, suspicious_doc_string, threshold=1):
        # Check overlap on 5-grams on suspicious document and candidate document
        sus_preprocessed = EngPreprocessing.preprocess2word(
            suspicious_doc_string)
        sus_grams = ngrams(sus_preprocessed, 5)
        sus_grams = [' '.join(grams) for grams in sus_grams]
        # print(sus_grams)
        # Define threshold overlap
        # threshold = 1
        check_snippet_based = []

        for candidate in search_results:
            if candidate['snippet'] == '':
                continue
            can_preprocessed = EngPreprocessing.preprocess2word(
                candidate['snippet'])
            can_grams = ngrams(can_preprocessed, 5)
            can_grams = [' '.join(grams) for grams in can_grams]
            overlap = [value for value in sus_grams if value in can_grams]

            if len(overlap) >= threshold:
                check_snippet_based.append(candidate)

        # print(len(check_snippet_based))
        return check_snippet_based

    @staticmethod
    def snippet_based_checking_vi(search_results, suspicious_doc_string, threshold=1):
        # Check overlap on 5-grams on suspicious document and candidate document
        sus_preprocessed = VnmPreprocessing.preprocess2word(
            suspicious_doc_string)
        sus_grams = ngrams(sus_preprocessed, 5)
        sus_grams = [' '.join(grams) for grams in sus_grams]
        # print(sus_grams)
        # Define threshold overlap
        # threshold = 1
        check_snippet_based = []

        for candidate in search_results:
            if candidate['snippet'] == '':
                continue
            can_preprocessed = VnmPreprocessing.preprocess2word(
                candidate['snippet'])
            can_grams = ngrams(can_preprocessed, 5)
            can_grams = [' '.join(grams) for grams in can_grams]
            overlap = [value for value in sus_grams if value in can_grams]

            if len(overlap) >= threshold:
                check_snippet_based.append(candidate)

        # print(len(check_snippet_based))
        return check_snippet_based
