from pds.reader.docx import DOCXReader
from pds.reader.pdf import PDFReader


def readInput(path):
    pdf_data = PDFReader.getPDFList(path)
    docx_data = DOCXReader.getDOCXList(path)
    input = pdf_data + docx_data
    if len(input) == 0:
        return []
    return input[0]
