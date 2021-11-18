from abc import ABC
from pds.reader.docx import DOCXReader
from pds.reader.pdf import PDFReader
from pds.pre_processing.eng_preprocessing import EngPreprocessing
from pds.pre_processing.vnm_preprocessing import VnmPreprocessing


class Document(ABC):
    @staticmethod
    def __createDocuments(fileObject, collection):
        content = fileObject.getContent()
        content_w = EngPreprocessing.preprocess2word(
            content) if collection == 'eng' else VnmPreprocessing.preprocess2word(content)
        content_s = EngPreprocessing.preprocess2sent(
            content) if collection == 'eng' else VnmPreprocessing.preprocess2sent(content)
        item = {'Title': fileObject.getTitle(),
                'Author': fileObject.getAuthor(),
                'Content': fileObject.getContent(),
                'Content-type': fileObject.getType(),
                'Created-time': fileObject.getDate(),
                'Content-word': content_w,
                'Content-sent': content_s}
        return item

    @classmethod
    def __pdf_push(cls, dbname, folder, collection):
        pdf_data = PDFReader.getPDFList(folder)
        pdf_docs = list(
            map(lambda data: cls.__createDocuments(data, collection), pdf_data))
        if(pdf_docs != []):
            collection_name = dbname[collection]
            collection_name.insert_many(pdf_docs)
        PDFReader.clean(pdf_data)

    @classmethod
    def __docx_push(cls, dbname, folder, collection):
        docx_data = DOCXReader.getDOCXList(folder)
        docx_docs = list(
            map(lambda data: cls.__createDocuments(data), docx_data))
        if(docx_docs != []):
            collection_name = dbname[collection]
            collection_name.insert_many(docx_docs)
        DOCXReader.clean(docx_data)

    @classmethod
    def push(cls, dbname, folder, collection):
        cls.__pdf_push(dbname, folder, collection)
        cls.__docx_push(dbname, folder, collection)

    @staticmethod
    def getCollection(dbname, colname):
        collection = dbname[colname]
        return collection.find()
