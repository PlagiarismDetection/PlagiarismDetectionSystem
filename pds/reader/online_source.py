import os
import requests
from bs4 import BeautifulSoup
from tika import parser

class OnlSource():
    def __init__(self, metadata, content):
        self.url = metadata['url']
        self.title = metadata['title']
        self.snippet = metadata['snippet']
        self.content = content

    def getUrl(self):
        return self.url

    def getTitle(self):
        return self.title

    def getSnippet(self):
        return self.getSnippet

    def getContent(self):
        return self.content


class ReadOnlSource():
    def __init__(self):
        pass

    @staticmethod
    def download_pdf_from_url(url, output_dir=''):
        if url.find('?') > 0:
            url = url[:url.find('?')]

        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(output_dir, os.path.basename(url))
            print('Downloading ', file_path, '...')
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print('Finish')
            return file_path

        # print('Cant download from ', url)
        return False

    @classmethod
    def read_pdf_from_url(cls, url):
        path = cls.download_pdf_from_url(url)
        if path:
            raw = parser.from_file(path)
            os.remove(path)
            return raw["content"]
        return False
        # print('Cant read ', url)

    @staticmethod
    def read_text_from_url(url):
        response = requests.get(url, verify=False)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # # get text
            # case 1: Get all text
            # text = soup.body.get_text()
            # case 2: Get all text in p tag
            text = ""
            all_para = soup.body.find_all("p")
            for para in all_para:
                text += para.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip()
                      for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text

        # print('Cant read ', url)
        return False

    @staticmethod
    def is_pdf_url(url):
        return url.endswith('.pdf')

    @classmethod
    def getOnlList(cls, searchlist):
        onlList = []
        skipWebLst = ['tailieumienphi.vn']
        skipTailLst = ['model', 'aspx']
        for searchres in searchlist:
            content = ''
            if searchres['url'].split('.')[-1] in skipTailLst or searchres['url'].split('/')[2] in skipWebLst:
                continue
            if cls.is_pdf_url(searchres['url']):
                content = cls.read_pdf_from_url(searchres['url'])
            else:
                content = cls.read_text_from_url(searchres['url'])

            if content:
                onlSrc = OnlSource(searchres, content)
                onlList.append(onlSrc)
        print('Read Online source Finish')
        return onlList
