from reader.DOCXReader import DOCXReader
from reader.PDFReader import PDFReader


def readInputs(folder):
    pdf_data = PDFReader.getPDFList(folder)
    docx_data = DOCXReader.getDOCXList(folder)
    return pdf_data + docx_data
