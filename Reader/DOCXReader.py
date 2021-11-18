import docx
import glob
from abc import ABC


class DOCX(ABC):
    def __init__(self, metadata, content):
        super().__init__()
        self.content_type = 'docx'
        self.title = metadata.title
        self.author = metadata.author
        self.creation_date = metadata.created
        self.content = content

    def getType(self):
        return self.content_type

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getDate(self):
        return self.creation_date

    def getContent(self):
        return self.content


class DOCXReader(ABC):
    @staticmethod
    def __getDocxText(obj):
        docx_paras = obj.paragraphs
        full = []
        for para in docx_paras:
            full.append(para.text)
        return '\n'.join(full)

    @classmethod
    def __getData(cls, folder):
        fileList = glob.glob('{}/*.docx'.format(folder))
        return list(map(lambda filename: docx.Document(filename), fileList))

    @classmethod
    def getDOCXList(cls, folder):
        dataList = cls.__getData(folder)
        docxList = []
        for data in dataList:
            doc = DOCX(data.core_properties, cls.__getDocxText(data))
            docxList.append(doc)
        return docxList

    @staticmethod
    def clean(lst):
        try:
            for doc in lst:
                del doc
        except:
            print('Type Error')
